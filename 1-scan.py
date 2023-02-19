# 20 febbraio 2023 - maurizio.conti@fablabromagna.org
# Esegue la scansione delle reti WiFi nelle vicinanze
#
import wifi

for network in wifi.radio.start_scanning_networks():
    print(network, network.ssid, network.channel)

wifi.radio.stop_scanning_networks()
