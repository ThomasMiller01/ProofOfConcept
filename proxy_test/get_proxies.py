import requests
from datetime import datetime
import pytz

proxies = []

for i in range(10):
    response = requests.get(
        "https://api.proxyorbit.com/v1/?token=Zhf0jvsvuSikxECdpElXmq9pOjaKd212R2oDJ-1dtLY")
    data = response.json()
    proxies.append(str(data["ip"]) + ":" + str(data["port"]))

with open("./proxies_" + datetime.now(pytz.timezone("Europe/Berlin")).strftime("%d_%m_%Y") + ".txt", "w") as f:
    f.write('\n'.join(proxies))
