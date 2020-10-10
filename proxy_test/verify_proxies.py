import requests
import os
import csv
import re


class VerifyProxies:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

        self.current_ip = self.get_current_ip()

        self.ip_regex = re.compile('^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')

        self.attemps = 2
        self.timeout = 3

    def verify(self):
        # format proxies
        proxy_list = self.get_proxies_formated(self.input_file)

        # verify proxies
        verified_proxies = []
        print("------------ verifying proxies ------------")
        print("- file: '" + self.input_file + "'")
        for proxy in proxy_list:
            verified_tmp = False
            for i in range(self.attemps):
                ip = self.verify_proxy(proxy[0], proxy[1])
                if "Error" not in ip:
                    verified = True if ip != self.current_ip and self.ip_regex.match(
                        ip) else False
                    if verified:
                        verified_tmp = True
                        break
            if verified_tmp:
                print(proxy[0] + " (" + ip + ") [" + str(proxy[1]) + "]: [+]")
                verified_proxies.append(proxy)
            else:
                print(proxy[0] + " (" + ip + ") [" +
                      str(proxy[1]) + "]: [-]")

        print("")

        # write verified proxies to file
        with open(self.output_file, "w", newline='', encoding="utf-8") as f:
            csv_writer = csv.writer(f, delimiter=',')
            pretty_proxy_list = [[proxy[0].split(':')[0], proxy[0].split(
                ':')[1], "HTTP" if proxy[1] == None else proxy[1]] for proxy in verified_proxies]
            pretty_proxy_list.insert(0, ['ip', 'port', 'type'])
            csv_writer.writerows(pretty_proxy_list)

    def get_proxies_formated(self, filename):
        filename = filename.replace('./', '').replace('../', '')
        file_extension = filename.split('.')[1]
        if file_extension == 'txt':
            with open(filename, 'r', encoding="utf-8") as f:
                proxy_list = [(x.replace('\n', ''), None)
                              for x in f.readlines()]
            return proxy_list
        elif file_extension == 'csv':
            proxy_data = []
            with open(filename, "r", encoding="utf-8") as f:
                csv_reader = csv.reader(f, delimiter=',')
                i = 0
                for row in csv_reader:
                    if i == 0:
                        headers = [x.lower() for x in row]
                        ip_index = headers.index('ip')
                        port_index = headers.index('port')
                        type_index = headers.index('type')
                        i += 1
                    else:
                        proxy_data.append(
                            (row[ip_index] + ':' + row[port_index], row[type_index]))
            return proxy_data

    def verify_proxy(self, proxy, proxy_type):
        if proxy_type == None or proxy_type == 'None' or proxy_type.lower() == 'http' or 'http ' in proxy_type.lower():
            response = self.verify_http_proxy(proxy)
        elif 'https' in proxy_type.lower():
            response = self.verify_https_proxy(proxy)
        elif 'socks4' in proxy_type.lower().replace(' ', ''):
            response = self.verify_socks4_proxy(proxy)
        elif proxy_type.lower().replace(' ', '') == 'socks5':
            response = self.verify_socks5_proxy(proxy)
        else:
            response = "Unknown-Type-Error"
        if 'Error' in response:
            return response
        elif response.status_code != 200:
            return "Error"
        try:
            ip = response.json()["ip"]
        except Exception as e:
            return "Json-Error"
        return ip

    def verify_http_proxy(self, proxy):
        return self.run_request('http://api.ipify.org?format=json', {"http": "http://" + proxy})

    def verify_https_proxy(self, proxy):
        return self.run_request('https://api.ipify.org?format=json', {"https": "https://" + proxy})

    def verify_socks4_proxy(self, proxy):
        return self.run_request('http://api.ipify.org?format=json', {"http": "socks4://" + proxy})

    def verify_socks5_proxy(self, proxy):
        return self.run_request('http://api.ipify.org?format=json', {"http": "socks5://" + proxy})

    def get_current_ip(self):
        session = requests.Session()
        data = session.get("https://api.ipify.org?format=json")
        session.close()
        return data.json()["ip"]

    def run_request(self, url, proxy):
        session = requests.Session()
        session.proxies = proxy
        try:
            data = session.get(url, timeout=self.timeout)
        except Exception as e:
            return "Error"
        session.close()
        return data
