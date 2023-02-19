# 20 febbraio 2023 - maurizio.conti@fablabromagna.org
# Si collega al WiFi e chiama L'URL di una GoogleSheet Application
#
# (Versione semplificata)

import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests

TEXT_URL = "https://script.google.com/macros/s/AKfycbwkgK96UqbcgXljbcDItEazQRp5whC2-IrXuPreZP7F7ppgNrJfBLLXfLDnAapFQz5Ehg/exec?temperatura=21.2"

try:
    from secrets import secrets

except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to %s"%secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!"%secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

print("Fetching text from", TEXT_URL)

print("-" * 40)

try:
    response = requests.get(TEXT_URL)
    print(response)
except OSError:
    print("Errore di connessione... controlla url.")

print("-" * 40)

    