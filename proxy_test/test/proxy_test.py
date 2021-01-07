import requests

from proxy_utilities import Proxy_Util

def get_current_ip():
    session = requests.Session()
    data = session.get("https://api.ipify.org?format=json")
    session.close()
    return data.json()["ip"]

if __name__ == "__main__":
    print("started")
    proxy_util = Proxy_Util("./files/proxies.txt", "./files/proxy_config.json")

    current_ip = get_current_ip()
    
    data = proxy_util.get("https://api.ipify.org?format=json")
    
    if 'Exception' in str(data):
        raise data
    
    print(current_ip)
    print(data.json()["ip"])

    # data = proxy_util.get("https://www.ebay-kleinanzeigen.de/")
    
    # if 'Exception' in str(data):
    #     raise data

    # print(data.status_code)