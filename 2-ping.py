# 20 febbraio 2023 - maurizio.conti@fablabromagna.org
# Si collega al WiFi ed esegue un ping a google.com
#

import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests

try:
    from secrets import secrets

except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to %s"%secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!"%secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))
