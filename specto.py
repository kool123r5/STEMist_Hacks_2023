import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import signal
from scipy.io import wavfile
from pydub import AudioSegment

def spectrogram(file):
  sound = AudioSegment.from_wav(file)
  sound = sound.set_channels(1)
  sound.export(file, format="wav")
  sample_rate, samples = wavfile.read(file)
  frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
  plt.pcolormesh(times, frequencies, spectrogram, shading='gouraud')
  plt.ylim((0, 800))
  plt.ylabel('Frequency [Hz]')
  plt.xlabel('Time [sec]')
  actual_name = file.split('.')[0]
  plt.axis('off')
  plt.savefig(f'{actual_name}.png', bbox_inches='tight')

