# Example: ASK OOK demodulation
from scipy import signal
import numpy as np

def demodulate_ask(iq_samples, sample_rate):
    # Compute magnitude (envelope detection)
    magnitude = np.abs(iq_samples)

    # Low-pass filter
    b, a = signal.butter(5, 100000, fs=sample_rate)
    filtered = signal.filtfilt(b, a, magnitude)

    # Threshold
    threshold = np.mean(filtered)
    bits = (filtered > threshold).astype(int)

    return bits

# Load IQ file
iq_data = np.fromfile("capture_433MHz.iq", dtype=np.complex64)
bits = demodulate_ask(iq_data, sample_rate=2e6)
