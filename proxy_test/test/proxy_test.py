import requests

from proxy_utilities import Proxy_Util

def get_current_ip():
    session = requests.Session()
    data = session.get("https://api.ipify.org?format=json")
    session.close()
    return data.json()["ip"]

if __name__ == "__main__":
    print("started")
    proxy_util = Proxy_Util("./files/proxies_2.txt", "./files/proxy_config.json")

    current_ip = get_current_ip()
    
    data = []
    for i in range(12):
        result = proxy_util.get("https://api.ipify.org?format=json")
        data.append(result)
    
    if 'Exception' in str(data):
        raise data
    
    print(current_ip)
    print(data.json()["ip"])

    proxy_util_2 = Proxy_Util("./files/proxies_3.txt", "./files/proxy_config.json")

    data_2 = proxy_util_2.get("https://www.ebay-kleinanzeigen.de/")
    
    if 'Exception' in str(data_2):
        raise data_2

    print(data_2.status_code)