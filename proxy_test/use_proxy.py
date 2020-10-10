import requests
from requests_toolbelt.adapters import source
import random


class Proxies_Util:
    def __init__(self):
        self.proxies = self.load_proxies("./proxies_tmp.txt")
        self.headers = [
            # Firefox 77 Mac
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            },
            # Firefox 77 Windows
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            },
            # Chrome 83 Mac
            {
                "Connection": "keep-alive",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Dest": "document",
                "Referer": "https://www.google.com/",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
            },
            # Chrome 83 Windows
            {
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Referer": "https://www.google.com/",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9"
            }
        ]
        self.session = requests.Session()

    def get(self, url):
        for i in range(10):
            data = self.use_proxy(url)
            if self.validate_request(data):
                return data
        return None

    def validate_request(self, data):
        if data.status_code == 200:
            return True
        else:
            return False

    def use_proxy(self, url):
        # get random proxy
        proxy = self.get_random_proxy()
        if proxy:
            username_password = proxy['username'] + ':' + \
                proxy['password'] + '@' if 'username' in proxy else ''
            proxies = {
                'http': 'http://' + username_password + proxy['ip'] + ':' + proxy['port'],
                # 'https': 'https://' + username_password + proxy['ip'] + ':' + proxy['port']
            }
            headers = self.get_random_headers()

            # do request
            data = self.session.get(headers=headers, proxies=proxies, url=url)
            return data
        else:
            return None

    def get_random_proxy(self):
        return random.choice(self.proxies)

    def get_random_headers(self):
        return random.choice(self.headers)

    def load_proxies(self, filename):
        # open file
        with open(filename, "r", encoding="utf-8") as f:
            proxies_tmp = f.readlines()
        proxies_tmp = [x.replace('\n', '') for x in proxies_tmp]
        # parse proxy data
        if proxies_tmp:
            # if username and password in proxy
            if ';' in proxies_tmp[0]:
                proxies = [{
                    'ip': x.split(':')[0],
                    'port': x.split(':')[1].split(';')[0],
                    'username': x.split(';')[1].split(':')[0],
                    'password': x.split(';')[1].split(':')[1]
                } for x in proxies_tmp]
            else:
                proxies = [{
                    'ip': x.split(':')[0],
                    'port': x.split(':')[1],
                } for x in proxies_tmp]
            # have to be removed
            proxies = [x for x in proxies if '#' not in x['ip']]
            return proxies
        else:
            return []


proxies_Util = Proxies_Util()
data = proxies_Util.get('http://www.ebay-kleinanzeigen.de/')
pass
