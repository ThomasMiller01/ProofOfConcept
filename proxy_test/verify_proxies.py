import requests
import os


def run_request(url, proxy):
    session = requests.Session()
    session.proxies = {
        "http": "http://" + proxy,
    }
    try:
        data = session.get(url, timeout=2)
    except Exception as e:
        return "Error"
    session.close()
    return data


def verify_proxy(proxy):
    response = run_request('http://api.ipify.org?format=json', proxy)
    if response == "Error" or response.status_code != 200:
        return "Error"
    try:
        ip = response.json()["ip"]
    except Exception as e:
        return "Error"
    return ip


with open("./proxy-list-de.txt", "r") as f:
    proxy_list = [x.replace('\n', '') for x in f.readlines()]

verified_proxies = []

print("------------ verifying proxy ... ------------")
for proxy in proxy_list:
    ip = verify_proxy(proxy)
    if ip == "Error":
        print(proxy + ": [Error]")
    else:
        verified = True if ip == proxy.split(":")[0] else False
        if verified:
            print(proxy + " (" + ip + "): [+]")
            verified_proxies.append(proxy)
        else:
            print(proxy + " (" + ip + "): [-]")
print("")

already_verified = []

with open("./proxies.txt", "r") as f:
    already_verified = [x.replace('\n', '') for x in f.readlines()]

all_proxies = []

for proxy in verified_proxies:
    if already_verified.count(proxy) == 0:
        all_proxies.append(proxy)

all_proxies.extend(already_verified)

with open("./proxies.txt", "w") as f:
    f.write('\n'.join(all_proxies))
