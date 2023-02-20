# 20 febbraio 2023 - maurizio.conti@fablabromagna.org
# Si collega al WiFi ed esegue un ping a google.com
#

import ipaddress
import wifi

# Verifico l'esistenza del file secrets.py
try:
    from secrets import secrets

except ImportError:
    print("Non trovo il file secrets.py con le password del WiFI.")
    raise

# Mi connetto usando SSID e pwd che trovo nel file secrets.py
print( "Mi connetto a " + secrets["ssid"] )
wifi.radio.connect( secrets["ssid"], secrets["password"] )
print("OK. Sono connesso a " + secrets["ssid"])

print( "Il mio ip ", wifi.radio.ipv4_address )

# il mio mac in formato numero
strMac=""
for i in wifi.radio.mac_address:
    strMac += str(hex(i))[2:]
    
print( "Il mio mac: ", strMac)

ipv4 = ipaddress.ip_address("8.8.4.4")
print( "Ping google.com in " + str(wifi.radio.ping(ipv4)*1000) + " ms.")
