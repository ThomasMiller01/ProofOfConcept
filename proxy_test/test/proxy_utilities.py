import requests
import random
import json
import secrets
from urllib.parse import urlparse

from errors import ProxyRequestError, InvalidProxy


class Proxy_Util:
    """Proxy Utility

    Full proxy-rotator and random header generator.    

    :param proxy_filename: The path to the proxy file. It is a .txt file and each line contains one proxy and the file must have the following structure: ``ip:port:username:password``. ``username`` and ``password`` are `optional`.
    :type proxy_filename: str

    :param header_filename: The path to the header_config file. It is a .json file and must have the folowing structure: ``{ "header": { "user_agents": ["user_agent_here"], "referer": ["referer_here"] } }``.

    :param proxies: list of Proxy object
    :type proxies: list[Proxy]

    :param header_config: list of header user_agents and referer
    :type header_config: dict
    """

    def __init__(self, proxy_filename, header_filename):
        self.proxies = self.load_proxies(proxy_filename)
        self.header_config = self.load_header_config(header_filename)

        self.iter = iter(self.proxies)

    def get(self, url, verify=True):
        """ Make a request to a url.

        If a proxy failes, a new request with a new proxy will be made. At most 5 requests will be made, before a ``ProxyError`` will be returned.

        To make a proxy-request, ``use_proxy`` will be called.

        :param url: the url that will be fetched
        :type url: str

        :param verify: bool, if the requests should be made verified and for example ignore wrong ssl-certificates
        :type verify: bool

        :return: If a requests succeeds, the request result will be returned, otherwise a ProxyError containing all failed proxies will be returned
        :rtype: requests.Response or ProxyError        
        """
        usedProxies = []
        for i in range(1):
            data, proxy = self.use_proxy(url, verify)
            usedProxies.append({'proxy': proxy, 'data': data})
            if data and self.validate_request(data):
                print("proxy", proxy)
                return data        

        # parse usedProxies
        usedProxies_parsed = []
        for usedProxy in usedProxies:
            data = usedProxy['data'].__class__.__name__ if 'Exception' in str(usedProxy['data']) else 'HTTP [' + str(usedProxy['data'].status_code) + ']'
            proxy = {'ip': usedProxy['proxy'].ip, 'port': usedProxy['proxy'].port, 'username': usedProxy['proxy'].username, 'password': usedProxy['proxy'].password}
            usedProxies_parsed.append({'proxy': proxy, 'message': data})

        if 'Exception' in str(data):
            data.proxies = usedProxies
            return data

        return ProxyRequestError(url, usedProxies_parsed)

    def validate_request(self, data):
        """Validates a request by looking at the status_code

        :param data: the request that should be verified, can also be an ``Exception``
        :type data: requests.Response or Exception

        :return: ``True`` if the ``status_code`` is 200 and data is not an ``Exception``, otherwise ``False``
        :rtype: bool
        """
        if 'Exception' in str(data) or data.status_code != 200:
            return False
        else:
            return True

    def use_proxy(self, url, verify=True):
        """ Make a proxy request.

        Makes a request to a url, using a random proxy from the proxy-rotator ``get_random_proxy`` and a random header ``get_random_header``.

        :param url: the url that will be fetched
        :type url: str

        :param verify: bool, if the requests should be made verified and for example ignore wrong ssl-certificates
        :type verify: bool

        :return: If the request succeeds, the request response and the proxy will be returned. If it fails a ``ProxyError`` and the proxy will be returned. If the proxies are not loaded beforehand, ``None, None`` will be returned.
        :rtype: (requests.Response, Proxy) or (ProxyError, Proxy) or (None, None)
        """

        # get random proxy
        proxy = self.get_random_proxy()
        if proxy:
            username_password = proxy.username + ':' + \
                proxy.password + '@' if proxy.username else ''
            proxies = {
                'http': 'http://' + username_password + proxy.ip + ':' + proxy.port,
                'https': 'https://' + username_password + proxy.ip + ':' + proxy.port
            }
            headers = self.get_random_headers(url)

            param_joiner = "&" if url.count("?") > 0 else "?"

            constructed_url = url + param_joiner + self.build_block(random.randint(3, 10)) + "=" + self.build_block(random.randint(3, 10))

            # do request
            try:
                data = requests.get(headers=headers, proxies=proxies, url=constructed_url, verify=verify)
            except Exception as e:
                return InvalidProxy(url, [], e), proxy
            return data, proxy
        else:
            return None, None

    def get_random_proxy(self):
        """ ProxyRotator, returns a random proxy.

        Each call the next network will be selected and a random proxy from that network will be returned. Once all networks are cycled through, the rotator starts again with the first network.        

        :return: Random Proxy object
        :rtype: Proxy

        """
        _next = next(self.iter, None)
        if _next:
            network = _next
        else:
            self.iter = iter(self.proxies)
            network = next(self.iter, None)
        _proxies = self.proxies[network]
        return random.choice(_proxies)

    def get_random_headers(self, host_url):
        """Get a random header.

        A header has the following structure:

        .. code-block:: json

            {
                "User-Agent": "random_user_header",
                "Cache-Control": "no-cache",
                "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                "Referer": "random_referer + random_url_safe_string",
                "Keep-Alive": "random_integer_from_range [110 - 160]",
                "Connection": "keep-alive",        
                "Host": "host_url"    
            }        

        :param host_url: the url that will be fetched using the header
        :type host_url: type

        :return: random header dict
        :rtype: dict
        """
        user_agent = random.choice(self.header_config["user_agents"])
        referer = random.choice(self.header_config["referer"])
        host = urlparse(host_url).hostname
        header = {
            "User-Agent": user_agent,
            "Cache-Control": "no-cache",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
            "Referer": referer + self.build_block(random.randint(5, 20)),
            "Keep-Alive": str(random.randint(110, 160)),
            "Connection": "keep-alive",
            "Host": host
        }
        return header

    def load_header_config(self, header_config):
        """Loads a header_config file.

        :param header_config: path to the header_config file
        :type header_config: str

        :return: Returns a dict with user_agents and referers from the config file
        :rtype: dict
        """

        # open file and read data and parse as json
        with open(header_config, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        headers = json_data["header"]

        return {
            "user_agents": headers["user_agents"],
            "referer": headers["referer"],
        }

    def load_proxies(self, filename):
        """Parses and loads a proxies file.

        :param filename: path to the proxies file
        :type filename: str

        :return: Returns a dict with proxies grouped by their network. The key is each network and the value is a list of proxies corresponding to that network.
        :rtype: dict
        """
        # open file
        with open(filename, "r", encoding="utf-8") as f:
            proxies_tmp = f.readlines()
        proxies_tmp = [x.replace('\n', '') for x in proxies_tmp]
        # parse proxy data
        if proxies_tmp:
            # if username and password in proxy
            if len(proxies_tmp[0].split(":")) > 2:
                proxies = [Proxy(x.split(':')[0], x.split(':')[1], x.split(':')[2], x.split(':')[3]) for x in proxies_tmp]
            else:
                proxies = [Proxy(x.split(':')[0], x.split(':')[1]) for x in proxies_tmp]
            # filter unused proxies
            proxies = [x for x in proxies if '#' not in x.ip]
            # sort by network
            proxies_dict = {}
            for proxy in proxies:
                network = '.'.join(proxy.ip.split('.')[:-1:])
                if network in proxies_dict:
                    proxies_dict[network].append(proxy)
                else:
                    proxies_dict[network] = [proxy]
            return proxies_dict
        else:
            return {}

    def build_block(self, size):
        """Creates a url-safe string that can be used to randomize urls.        

        :param size: size of the string
        :type size: int

        :return: returns a url-safe string
        :rtype: str
        """

        return secrets.token_urlsafe(size)


class Proxy:
    """ Proxy class that can store a proxy.

    :param ip: ip-address of the proxy
    :type ip: str

    :param port: port of the proxy
    :type port: str

    :param username: username to authenticate with the proxy
    :type username: str, optional

    :param password: password to authenticate with the proxy
    :type password: str, optional    
    """

    def __init__(self, ip, port, username=None, password=None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
