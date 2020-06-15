import requests
import csv


class TestProxies:
    def __init__(self, proxies):
        self.proxies = proxies

        self.timeout = 3

    def test_proxies(self):
        print("------------ thomasmiller.info ------------")
        for proxy in self.proxies:
            self.run_request_thomasmiller_info(proxy)
        print("")

        print("------------ google ------------")
        for proxy in self.proxies:
            self.run_request_google(proxy)
        print("")

        print("------------ ebay_kleinanzeigen ------------")
        for proxy in self.proxies:
            self.run_request_ebay_kleinanzeigen(proxy)
        print("")

    def run_request_thomasmiller_info(self, proxy):
        response = self.test_proxy(
            "://api.thomasmiller.info/", proxy[0], proxy[1])
        if 'Error' in response:
            print(proxy[0] + ": [" + response + "]")
        elif response.text == "api test index.html":
            print(proxy[0] + ": [+]")
        else:
            print(proxy[0] + ": [-]")

    def run_request_google(self, proxy):
        response = self.test_proxy("://google.com", proxy[0], proxy[1])
        if "Error" in response:
            print(proxy[0] + ": [" + response + "]")
        elif response.status_code != 200:
            print(proxy[0] + ": [-]")
        else:
            print(proxy[0] + ": [+]")

    def run_request_ebay_kleinanzeigen(self, proxy):
        response = self.test_proxy(
            "://www.ebay-kleinanzeigen.de/", proxy[0], proxy[1])
        if "Error" in response:
            print(proxy[0] + ": [" + response + "]")
        elif "Access denied" in response.text or response.status_code != 200:
            print(proxy[0] + ": [-] (" + response.reason + ")")
        else:
            print(proxy[0] + ": [+]")

    def test_proxy(self, url, proxy, proxy_type):
        if proxy_type == None or proxy_type == 'None' or proxy_type.lower() == 'http' or 'http ' in proxy_type.lower():
            response = self.test_http_proxy(url, proxy)
        elif 'https' in proxy_type.lower():
            response = self.test_https_proxy(url, proxy)
        elif 'socks4' in proxy_type.lower().replace(' ', ''):
            response = self.test_socks4_proxy(url, proxy)
        elif proxy_type.lower().replace(' ', '') == 'socks5':
            response = self.test_socks5_proxy(url, proxy)
        else:
            response = "Unknown-Type-Error"
        return response

    def test_http_proxy(self, url, proxy):
        return self.run_request("http" + url, {"http": "http://" + proxy})

    def test_https_proxy(self, url, proxy):
        return self.run_request("https" + url, {"https": "https://" + proxy})

    def test_socks4_proxy(self, url, proxy):
        return self.run_request("http" + url, {"http": "socks4://" + proxy})

    def test_socks5_proxy(self, url, proxy):
        return self.run_request("http" + url, {"http": "socks5://" + proxy})

    def run_request(self, url, proxy):
        session = requests.Session()
        session.proxies = proxy
        try:
            data = session.get(url, timeout=self.timeout)
        except Exception as e:
            return "Error"
        session.close()
        return data
