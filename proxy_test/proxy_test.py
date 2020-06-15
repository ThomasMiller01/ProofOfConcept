import requests
import os
from verify_proxies import VerifyProxies
from test_proxies import TestProxies

files = [
    (
        "./proxies/spys-socks-proxy-list.csv",
        "./verified_proxies/spys-socks-proxy-list_verified.csv"
    ),
]

verify = False
test = True

for proxy_file in files:
    verifyProxies = VerifyProxies(proxy_file[0], proxy_file[1])

    if verify:
        verifyProxies.verify()

    print("... results saved!")

    if test:
        proxies = verifyProxies.get_proxies_formated(proxy_file[1])
        testProxies = TestProxies(proxies)
        testProxies.test_proxies()

    print("... tests done!")


print("")
print("... everything done ...")
