import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import signal
from scipy.io import wavfile
import random

def spectrogram(file):
  sample_rate, samples = wavfile.read(file)
  frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

  plt.pcolormesh(times, frequencies, spectrogram, shading='gouraud')
  plt.ylim((0, 800))
  plt.ylabel('Frequency [Hz]')
  plt.xlabel('Time [sec]')
  # plt.title(file)
  actual_name = file.split('/')[-1].split('.')[0]
  # print(actual_name)
  # plt.savefig(f'trainingData/Gun/{actual_name}.png', bbox_inches='tight')
  plt.axis('off')
  plt.savefig(f'/Users/kushalb/Documents/VSCode/NeuralNetworkForSTEMistHacks/trainData/Gun/{actual_name}.png', bbox_inches='tight')
  # plt.savefig('ok.png', bbox_inches='tight')
  # plt.show()

# spectrogram('m16_6.wav')
count = 0
folders = os.listdir('/Users/kushalb/Documents/VSCode/NeuralNetworkForSTEMistHacks/Kimber45_iPhone')
for file in folders:
  count = count + 1
  # file = folders[random.randint(100, 419)]
  print(count, file)
  spectrogram('/Users/kushalb/Documents/VSCode/NeuralNetworkForSTEMistHacks/Kimber45_iPhone/' + file)