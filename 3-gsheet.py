# 20 febbraio 2023 - maurizio.conti@fablabromagna.org
# Si collega al WiFi e chiama L'URL di una GoogleSheet Application
#
# (Versione semplificata)
# Punta a questo GSHeet
# https://cutt.ly/N3MHPom

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

print( "Connecting to " + secrets["ssid"] )
wifi.radio.connect( secrets["ssid"], secrets["password"] )

print("Connected to " + secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

# le connessioni via HTTP si effettuano grazie ai socket.
# i socket in circuit python si gestiscono con la libreria socketpool
pool = socketpool.SocketPool(wifi.radio)

# una volta creato il socket, si attiva una sessione
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# il mio mac in formato numero
strMac=""
for i in wifi.radio.mac_address:
    strMac += str(i)        

# L'URL da chiamare
TEXT_URL = "https://script.google.com/macros/s/AKfycbzEZOXTxybDFQ8qzm8bmE6ai912bBdUBpvkk0_84kIeXMUJw-iZ95IfGufW_3Vz6gMnww/exec?temperatura=21.2&nome=" + strMac

print("Fetching text from", TEXT_URL)
print("-" * 40)


try:	
    # una sessione contiene i verbi HTTP come GET
    response = requests.get( TEXT_URL )
    print( response.text )
    response.close() # chiude la connessione
    
except OSError:
    print("Errore di connessione... controlla url.")

print("-" * 40)

    