# Wideband scan to identify frequency
hackrf_sweep -f 300:900 -w 20000000 > sweep.csv

# Identify active frequency (e.g., 433.92 MHz)
# Capture IQ samples
hackrf_transfer -r capture_433MHz.iq -f 433920000 -s 2000000 -g 20 -l 32 -a 1 -n 10000000
