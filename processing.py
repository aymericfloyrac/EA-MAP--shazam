#basically HP filter, fourier transform and window function => create a relevant spectrogram 

import numpy as np


def window(...):
  return audiow
  
  
def HPfilter(audiow,threshold):
  ftaudio=np.array(np.fft(audiow))
  for coef in ftaudio:
    if coef<threshold:
      coef=0
  return ftaudio
  
  
  
