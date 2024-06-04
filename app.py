# %%

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band', analog=True)
    y = lfilter(b, a, data)
    return y

average_frequencies = [
    251, 376, 501, 626, 751, 876, 1001, 1126, 1251, 1376,
    1501, 1626, 1751, 1876, 2001, 2126, 2251, 2376, 2501,
    2626, 2751, 2876
]

bandwidth = 1

input_filename = 'music.wav'
output_filename = 'filtered.wav'
fs, data = wavfile.read(input_filename)

if len(data.shape) == 2:
    data = np.mean(data, axis=1)

filtered_signal = np.zeros_like(data, dtype=np.float64)
for freq in average_frequencies:
    lowcut = freq - bandwidth / 2
    highcut = freq + bandwidth / 2
    filtered_signal += bandpass_filter(data, lowcut, highcut, fs)

filtered_signal = np.int16(filtered_signal / np.max(np.abs(filtered_signal)) * 32767)

wavfile.write(output_filename, fs, filtered_signal)