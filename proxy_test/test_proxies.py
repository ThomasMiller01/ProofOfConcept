import requests
import csv


class TestProxies:
    def __init__(self, proxies):
        self.proxies = proxies

        self.attemps = 2
        self.timeout = 3

    def test(self):
        print("------------ testing proxies ------------")
        for proxy in self.proxies:
            print(proxy[0] + " [" + proxy[1] + "]:")
            resThomasmillerInfo = self.run_test_attemps(
                self.run_request_thomasmiller_info, proxy)
            print("  - thomasmiller.info: [" + resThomasmillerInfo + "]")
            resGoogle = self.run_test_attemps(self.run_request_google, proxy)
            print("  - google: [" + resGoogle + "]")
            resEbaykleinanzeigen = self.run_test_attemps(
                self.run_request_ebay_kleinanzeigen, proxy)
            print("  - EbayKleinanzeigen: [" + resEbaykleinanzeigen + "]")
            resEmp = self.run_test_attemps(
                self.run_request_emp, proxy)
            print("  - Emp: [" + resEmp + "]")

    def run_test_attemps(self, method, proxy):
        tested_positiv_tmp = False
        for i in range(self.attemps):
            response = method(proxy)
            if "Error" not in response:
                tested_positiv = True if response == '+' else False
                if tested_positiv:
                    verified_tmp = True
                    break
        return response

    def run_request_thomasmiller_info(self, proxy):
        response = self.test_proxy(
            "://api.thomasmiller.info/", proxy[0], proxy[1])
        if 'Error' in response:
            return response
        elif response.text == "api test index.html":
            return "+"
        else:
            return "-"

    def run_request_google(self, proxy):
        response = self.test_proxy("://google.com", proxy[0], proxy[1])
        if "Error" in response:
            return response
        elif response.status_code == 200:
            return "+"
        else:
            return "-"

    def run_request_ebay_kleinanzeigen(self, proxy):
        response = self.test_proxy(
            "://www.ebay-kleinanzeigen.de/", proxy[0], proxy[1])
        if "Error" in response:
            return response
        elif "Access denied" in response.text or response.status_code != 200:
            return "-"
        else:
            return "+"

    def run_request_emp(self, proxy):
        response = self.test_proxy("://www.emp.de/", proxy[0], proxy[1])
        if "Error" in response:
            return response
        elif response.status_code == 200:
            return "+"
        else:
            return "-"

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
