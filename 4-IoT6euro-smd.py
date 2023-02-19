# 20 febbraio 2023 - maurizio.conti@fablabromagna.org
#
# Accede alla WEB-API di School Maker Day
# (Versione completa)

# queste lib sono già dentro al firmware di Circuit Python
import ipaddress
import ssl
import wifi
import socketpool
import microcontroller
import time

# Questa invece si scarica da qui
# 
import adafruit_requests

# Manuale della WebAPI
# http://www.schoolmakerday.it/logger/

# Mi connetto usando SSID e pwd che trovo nel file secrets.py
from secrets import secrets
print( "Mi connetto a %s"%secrets["ssid"] )
wifi.radio.connect( secrets["ssid"], secrets["password"] )

print( "Connesso a %s!"%secrets["ssid"])
print("Il mio IP: ", wifi.radio.ipv4_address)
print("Il mio MAC:", [hex(i) for i in wifi.radio.mac_address])

# adafruit_requests serve per eseguire delle connessioni HTTP usando le socket
# La classe prevede anche connessioni HTTPS quindi usa SSL
#
# In sistensi, per fare una chiama HTTP GET, ci serve
# - un socket (oggetto socketpool)
# - un contesto ssl creato con un certificato autogenerato
# - una sessione HTTP/HTTPS 
pool = socketpool.SocketPool( wifi.radio )
context = ssl.create_default_context()
requests = adafruit_requests.Session(pool, context)

# La parte di inizializzazione del client HTTP è finita
# Ora la usiamo
print( "-" * 40 )

# Queste lib servono per la decodifica del JSON
import json
import board

# Qui mi preparo qualche URL utile...
URL_BASE = "http://www.schoolmakerday.it/logger"
URL_GET_TIME = URL_BASE + "/time.php"
URL_LOG = URL_BASE + "/log.php"
URL_GET_VALUE = URL_BASE + "/getvalue.php"

# Non serve a molto, solo per capire che il ciclo
# principale sta ancora girando
NUMERO_DI_GIRO = 0

# per usare il led BUILT_IN uso la lib digitalio
# quindi la devo importare
import digitalio
led = digitalio.DigitalInOut( board.LED )
led.direction = digitalio.Direction.OUTPUT

# ciclo principale
while True:
    
    NUMERO_DI_GIRO += 1
    
    # Legge la temperatura interna della CPU
    temperatura = str(microcontroller.cpu.temperature)
    
    # Invia la temperatura al logger chiamando un URL nella forma
    # http://www.schoolmakerday.it/logger/log.php?key=temperatura&value=30.1
    #
    URL = URL_LOG + "?key=temperatura" + "&value=" + temperatura
    
    # Esegue la chiamata HTTP con il verbo "GET"
    response = requests.get( URL )
    #print( "Text Response: ", response.text )
    response.close()

    # Se vuoi vedere i dati registrati, punta il browser qui
    # http://www.schoolmakerday.it/logger/logview.php?key=temperatura
    # Oppure qui
    # http://www.schoolmakerday.it/logger/monitor.php
    
    ########################################################
    
    NOME_DEL_LED = "led1"
    
    #
    # Per leggere un valore dal cloud, formiamo un URL in questo modo
    # http://www.schoolmakerday.it/logger/getvalue.php?key=led1
    URL = URL_GET_VALUE + "?key=" + NOME_DEL_LED

    # e lo eseguiamo verbo "GET" di HTTP
    response = requests.get(URL)
    print( "GET on ", URL )
    print( "Text Response: ", response.text )

    # la tipica risposta a questa chiamata è un oggetto JSON con due valori
    # status e data.  Dopo aver verificato status per "OK", guardiamo il "value" di "data"
    # {
    #   "status":"OK",
    #   "data":{
    #        "key":"led1",
    #        "value":"0",
    #        "ts":"2023-02-12 17:55:46"
    #   }
    # }

    # Per farlo, decodifichiamo il json che ci è arrivato
    risposta = json.loads( response.text )
    
    # Ora, se lo stato è OK e i dati sono integri, procediamo
    if( risposta["status"] == "OK"
        and risposta["data"] is not None
        and risposta["data"]["value"] is not None
        ):

        # OK, ci siamo
        print( risposta["data"]["value"] )
        led.value = int(risposta["data"]["value"])
    
   
    print( "Giro " + str(NUMERO_DI_GIRO) )
    time.sleep(1.5)


