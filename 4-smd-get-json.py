# 20 febbraio 2023 - maurizio.conti@fablabromagna.org
#
# Accede alla WEB-API di School Maker Day
# Passo 2: Esegue la chiamata GET e la decodifica JSON
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

# Queste lib servono per la decodifica del JSON
import json
import board

# Esegue la chiamata HTTP con il verbo "GET"
response = requests.get( URL )

# dentro a response.text c'è una stringa JSON
print( "Text Response: ", response.text )

# Decodifichiamo il json che ci è arrivato
risposta = json.loads( response.text )

# risposta + un vettore con due stringhe "status" e "data"
print( "Risultato della chiamata: ", risposta["status"] )
print( "Time del server: ", risposta["data"] )

# "data" a sua volta è un vettore di stringhe
# possiamo quindi accedere ai valori interni con data["nomedelvalore"]
print( "ore: ", risposta["data"]["hour"] )
print( "minuti: ", risposta["data"]["minute"] )
print( "secondi: ", risposta["data"]["second"] )

# Sempre buona cosa deallocare le risorse legate alla connessione
response.close()


