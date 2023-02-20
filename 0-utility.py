# 20 febbraio 2023 - maurizio.conti@fablabromagna.org
# Esegue la scansione delle reti WiFi nelle vicinanze
#

# la lib con le risorse del micro
import microcontroller

# la temperatura interna del Pico, in formato stringa
temperatura = str( microcontroller.cpu.temperature )
print("Temperatura interna: " + temperatura )

import board
import digitalio
import time

# configuro il led a bordo
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# configuro il led su GP20
led20 = digitalio.DigitalInOut(board.GP20)
led20.direction = digitalio.Direction.OUTPUT

# lo accendo, aspetto 1 secondo, lo spengo
led20.value = 1
led.value = 1

time.sleep(1)

led20.value = 0
led.value = 0

while True:
    led.value = not led.value
    time.sleep(0.5)

