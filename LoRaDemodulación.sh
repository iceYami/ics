# Using gr-lora (GNU Radio LoRa decoder)
git clone https://github.com/rpp0/gr-lora
cd gr-lora
mkdir build && cd build
cmake ..
make
sudo make install

# Capture LoRa packets (use GNU Radio flowgraph or gr-lora examples)
# Frequency: 868 MHz (EU) or 915 MHz (US)
# Bandwidth: 125 kHz (typical)
# Spreading Factor: 7-12
