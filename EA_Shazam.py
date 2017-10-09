# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 14:25:16 2017

@author: aymer
"""

#étapes: 1) acquérir le son en temps continu 2)trouver un format d'utilisation
#3) processing (ttf aso) 4) comparaison avec la base de données 


import time,sys
import pyaudio


def acquisition():
   #currently gives an error "invalid input device"
   
   p=pyaudio.PyAudio()
   
   #parameters of sampling and quantitizing
   CHUNK = 1024
   FORMAT = pyaudio.paInt16
   CHANNELS = 2
   RATE = 44100
   RECORD_SECONDS = 5
   
   stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
	
   frames = []
   # here is how we actually get information 
   for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	   data = stream.read(CHUNK)
	   frames.append(data)
   print(frames[10])

   stream.stop_stream()
   stream.close()
   p.terminate()
   
   
def processing(data):
    #high pass filter
    
    return None
    
    
