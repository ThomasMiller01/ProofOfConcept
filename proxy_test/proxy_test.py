import requests
import os


def run_request(url, proxy):
    session = requests.Session()
    session.proxies = {
        "http": "http://" + proxy,
    }
    try:
        data = session.get(url, timeout=5)
    except Exception as e:
        return "Error"
    session.close()
    return data


def run_request_thomasmiller_info(proxy):
    response = run_request("http://api.thomasmiller.info/", proxy)
    if response == "Error":
        print(proxy + ": [Error]")
    elif response.text == "api test index.html":
        print(proxy + ": [+]")
    else:
        print(proxy + ": [-]")


def run_request_google(proxy):
    response = run_request("http://google.com", proxy)
    if response == "Error":
        print(proxy + ": [Error]")
    elif response.status_code != 200:
        print(proxy + ": [-]")
    else:
        print(proxy + ": [+]")


def run_request_ebay_kleinanzeigen(proxy):
    response = run_request(
        "http://www.ebay-kleinanzeigen.de/s-hot-toys-iron-man/k0", proxy)
    if response == "Error":
        print(proxy + ": [Error]")
    elif "Access denied" in response.text or response.status_code != 200:
        print(proxy + ": [-]")
    else:
        print(proxy + ": [+]")


with open("./proxies.txt", "r") as f:
    proxy_list = [x.replace('\n', '') for x in f.readlines()]

print("------------ thomasmiller.info ------------")
for proxy in proxy_list:
    run_request_thomasmiller_info(proxy)
print("")

print("------------ google ------------")
for proxy in proxy_list:
    run_request_google(proxy)
print("")

print("------------ ebay_kleinanzeigen ------------")
for proxy in proxy_list:
    run_request_ebay_kleinanzeigen(proxy)
print("")

print("... done")
