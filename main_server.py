from __future__ import print_function
import scipy, pylab
from scipy.io.wavfile import read
import sys
import peakpicker as pp
import fingerprint as fhash
import matplotlib
import numpy as np
import tdft

##VIRGINIE
import librosa

#TDFT parameters
windowsize = 0.008     #set the window size  (0.008s = 64 samples)
windowshift = 0.004    #set the window shift (0.004s = 32 samples)
fftsize = 1024         #set the fft size (if srate = 8000, 1024 --> 513 freq. bins separated by 7.797 Hz from 0 to 4000Hz)

#Peak picking dimensions
f_dim1 = 30
t_dim1 = 80
f_dim2 = 10
t_dim2 = 20
percentile = 70
base = 70 # lowest frequency bin used (peaks below are too common/not as useful for identification)
high_peak_threshold = 75
low_peak_threshold = 60

#Hash parameters
delay_time = 250      # 250*0.004 = 1 second
delta_time = 250*3    # 750*0.004 = 3 seconds
delta_freq = 128      # 128*7.797Hz = approx 1000Hz

#Time pair parameters
TPdelta_freq = 4
TPdelta_time = 2


def create_database():

    #Construct the audio database of hashes
    database = np.zeros((1,5))
    spectrodata = []
    peaksdata = []

    files = librosa.util.find_files('data')
    songs = []
    songnames = [(f.split('/')[-1]).split('.')[-2] for f in files]
    separator = '.'

    num_inputs = len(songnames)

    for i in range(num_inputs):
        songs.append(librosa.load(files[i]))

    for i in range(0,len(songs)):

        print('Analyzing '+str(songnames[i]))

        srate = songs[i][1]
        audio = songs[i][0]
        ##END VIRGINIE

        spectrogram = tdft.tdft(audio, srate, windowsize, windowshift, fftsize)
        time = spectrogram.shape[0]
        freq = spectrogram.shape[1]

        threshold = pp.find_thres(spectrogram, percentile, base)

        print('The size of the spectrogram is time: '+str(time)+' and freq: '+str(freq))
        spectrodata.append(spectrogram)

        peaks = pp.peak_pick(spectrogram,f_dim1,t_dim1,f_dim2,t_dim2,threshold,base)

        print('The initial number of peaks is:'+str(len(peaks)))
        peaks = pp.reduce_peaks(peaks, fftsize, high_peak_threshold, low_peak_threshold)

        print('The reduced number of peaks is:'+str(len(peaks)))


        peaksdata.append(peaks)

        #Calculate the hashMatrix for the database song file
        songid = i
        hashMatrix = fhash.hashPeaks(peaks,songid,delay_time,delta_time,delta_freq)

        #Add to the song hash matrix to the database
        database = np.concatenate((database,hashMatrix),axis=0)


    print('The dimensions of the database hash matrix: '+str(database.shape))
    database = database[np.lexsort((database[:,2],database[:,1],database[:,0]))]

    return database, songnames, songs



def analyze_sample(sample):

    srate = sample[1]  #sample rate in samples/second
    audio = sample[0]  #audio data

    spectrogram = tdft.tdft(audio, srate, windowsize, windowshift, fftsize)
    time = spectrogram.shape[0]
    freq = spectrogram.shape[1]

    print('The size of the spectrogram is time: '+str(time)+' and freq: '+str(freq))

    threshold = pp.find_thres(spectrogram, percentile, base)

    peaks = pp.peak_pick(spectrogram,f_dim1,t_dim1,f_dim2,t_dim2,threshold,base)

    print('The initial number of peaks is:'+str(len(peaks)))
    peaks = pp.reduce_peaks(peaks, fftsize, high_peak_threshold, low_peak_threshold)
    print('The reduced number of peaks is:'+str(len(peaks)))

    #Store information for the spectrogram graph
    samplePeaks = peaks
    sampleSpectro = spectrogram

    hashSample = fhash.hashSamplePeaks(peaks,delay_time,delta_time,delta_freq)
    print('The dimensions of the hash matrix of the sample: '+str(hashSample.shape))
    return hashSample



def song_id(hashSample, database, songs):
    timepairs = fhash.findTimePairs(database, hashSample, TPdelta_freq, TPdelta_time)

    #Compute number of matches by song id to determine a match
    numSongs = len(songs)
    songbins= np.zeros(numSongs)
    numOffsets = len(timepairs)
    offsets = np.zeros(numOffsets)
    index = 0
    for i in timepairs:
        offsets[index]=i[0]-i[1]
        index = index+1

        ##VIRGINIE i[2]
        #songbins[i[2]] += 1
        songbins[int(i[2])] += 1
        return np.argmax(songbins)
