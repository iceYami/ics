# Use hackrf_sweep for wideband scanning
hackrf_sweep -f 2400:2500 -w 20000000 -n 8192 > sweep_2.4GHz.csv

# Real-time spectrum display with gqrx
gqrx
# Set device: HackRF One
# Set frequency: 2450 MHz
# Set bandwidth: 20 MHz
