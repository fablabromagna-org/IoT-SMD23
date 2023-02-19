# 20 febbraio 2023 - maurizio.conti@fablabromagna.org
# Si collega al WiFi ed esegue un ping a google.com
#

import ipaddress
import wifi

try:
    from secrets import secrets

except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print( "Mi connetto a " + secrets["ssid"] )
wifi.radio.connect( secrets["ssid"], secrets["password"] )

# Se non ci sono stati errori, siamo qui
print( "Sono connesso a " + secrets["ssid"])
print( "Il mio ip ", wifi.radio.ipv4_address )

# il mio mac in formato numero
strMac=""
for i in wifi.radio.mac_address:
    strMac += str(hex(i))[2:]
    
print( "Il mio mac: ", strMac)

ipv4 = ipaddress.ip_address("8.8.4.4")
print( "Ping google.com in " + str(wifi.radio.ping(ipv4)*1000) + " ms.")
