# Scan 2.4 GHz ISM band (WirelessHART, Zigbee, WiFi)
rtl_power -f 2400M:2500M:100k -g 50 -i 1 -e 1h scan_2.4GHz.csv

# Visualize
python3 heatmap.py scan_2.4GHz.csv scan_2.4GHz.png

# Scan 915 MHz ISM band (LoRa, some Zigbee)
rtl_power -f 900M:930M:50k -g 50 -i 1 -e 30m scan_915MHz.csv
