# 20 febbraio 2023 - maurizio.conti@fablabromagna.org
#
# Accede alla WEB-API di School Maker Day
# Primo passo: Esegue solo la chiamata GET
#

# queste lib sono già dentro al firmware di Circuit Python
import ipaddress
import ssl
import wifi
import socketpool
import microcontroller
import time

# Questa invece si scarica da qui
# https://learn.adafruit.com/pages/20891/elements/3077480/download?type=zip
import adafruit_requests

# Manuale della WebAPI
# http://www.schoolmakerday.it/logger/

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

#######################################################
# ZONA in cui preparo il codice per la connessione
# Per fare una chiamata HTTP GET, servono tre cose:

# 1) un oggetto socket(di tipo socketpool)
pool = socketpool.SocketPool( wifi.radio )

# 2) un oggetto ssl (il certificato è dentro al core di CP)
context = ssl.create_default_context()

# 3) un oggetto in grado di eseguire chiamate HTTP/HTTPS 
requests = adafruit_requests.Session(pool, context)

# Fine ZONA in cui preparo il codice per la connessione
#######################################################

# Ci siamo
print( "-" * 40 )

# L'URL da chiamare
URL = "http://www.schoolmakerday.it/logger/time.php"

# Esegue la chiamata HTTP con il verbo "GET"
response = requests.get( URL )

# dentro a response.text c'è una stringa JSON
print( "Text Response: ", response.text )

# Sempre buona cosa deallocare le risorse legate alla connessione
response.close()


