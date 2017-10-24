'''
Music Identification Program (a.k.a. Shazam/Soundhound)
Proof of Concept
Bryant Moquist
'''

from __future__ import print_function
import scipy, pylab
#from scipy.io.wavfile import read
#import sys
import peakpicker as pp
import fingerprint as fhash
import matplotlib
import numpy as np
import os 
#import tdft

##VIRGINIE
from recording import record
from main_server import create_database, song_id, analyze_sample
import librosa

if __name__ == '__main__':
    ##VIRGINIE
    db_path=input("enter location of the database:  ")
    database, songnames, songs = np.load(db_path)
    ##END VIRGINIE

    try:
        while True:
            # Audio sample to be analyzed and identified
            print('Please enter an audio sample file to identify. Press CTRL+C if you want to stop.')

            userinput = record()
            sample = librosa.load(userinput)

            print('Analyzing the audio sample: '+str(userinput))

            hashSample = analyze_sample(sample)

            print('Attempting to identify the sample audio clip.')

            ###VIRGINIE
            index = song_id(hashSample, database, songs)

            # Identify the song
            print('The sample song is: '+str(songnames[index]))
            ###END VIRGINIE
    except KeyboardInterrupt:
        pass

    # # Plots
    # fig = []
    #
    # # Plot the magnitude spectrograms
    # for i in range(0,numSongs):
    #     fig1 = pylab.figure(i)
    #     peaks = peaksdata[i]
    #     pylab.imshow(spectrodata[i].T,origin='lower', aspect='auto', interpolation='nearest')
    #     pylab.scatter(*zip(*peaks), marker='.', color='blue')
    #     pylab.title(str(songnames[i])+' Spectrogram and Selected Peaks')
    #     pylab.xlabel('Time')
    #     pylab.ylabel('Frequency Bin')
    #     fig.append(fig1)
    #
    # #Show the figures
    # for i in fig:
    #     i.show()
    #
    # fig2 = pylab.figure(1002)
    # pylab.imshow(sampleSpectro.T,origin='lower', aspect='auto', interpolation='nearest')
    # pylab.scatter(*zip(*samplePeaks), marker='.', color='blue')
    # pylab.title('Sample File: '+str(userinput)+' Spectrogram and Selected Peaks')
    # pylab.xlabel('Time')
    # pylab.ylabel('Frequency Bin')
    # fig2.show()
    #
    # fig3 = pylab.figure(1003)
    # ax = fig3.add_subplot(111)
    #
    # ind = np.arange(numSongs)
    # width = 0.35
    # rects1 = ax.bar(ind,songbins,width,color='blue',align='center')
    # ax.set_ylabel('Number of Matches')
    # ax.set_xticks(ind)
    # xtickNames = ax.set_xticklabels(songnames)
    # matplotlib.pyplot.setp(xtickNames)
    # pylab.title('Song Identification')
    # fig3.show()
    #
    # pylab.show()
    #
    # print('The sample song is: '+str(songnames[np.argmax(songbins)]))
