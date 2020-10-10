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

        self.attemps = 3
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
                ip = self.verify_proxy(proxy[0], proxy[1][0], proxy[1][1])
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
                ':')[1], proxy[1][0], proxy[1][1]] for proxy in verified_proxies]
            pretty_proxy_list.insert(0, ['ip', 'port', 'username', 'password'])
            csv_writer.writerows(pretty_proxy_list)

    def get_proxies_formated(self, filename):
        filename = filename.replace('./', '').replace('../', '')        
        proxy_data = []
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()                
            lines = [x.replace("\n", "") for x in lines]
            proxy_data = [(x.split(';')[0], (x.split(';')[1].split(':'))) for x in lines]
        return proxy_data

    def verify_proxy(self, proxy, username, password):        
        # response = self.verify_https_proxy(proxy, username, password)        
        response = self.verify_http_proxy(proxy, username, password)        
        if 'Error' in response:
            return response
        elif response.status_code != 200:
            return "Error"
        try:
            ip = response.json()["ip"]
        except Exception as e:
            return "Json-Error"
        return ip

    def verify_https_proxy(self, proxy, username, password):
        usernamepassword = username + ':' + password + '@'
        return self.run_request('https://api.ipify.org?format=json', {"https": "https://" + usernamepassword + proxy})        

    def verify_http_proxy(self, proxy, username, password):
        usernamepassword = username + ':' + password + '@'
        return self.run_request('http://api.ipify.org?format=json', {"http": "http://" + usernamepassword + proxy})     

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

verifyProxies = VerifyProxies("E:\GitHub\Repositorys\Workspace\GermanCollectors_DiscordBot\GermanCollectors\src\GermanCollectors\data\settings\proxies.txt", "./verified_proxies/proxies_http.csv")

verifyProxies.verify()
print("... results saved!")