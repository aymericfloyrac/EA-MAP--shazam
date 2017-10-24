import numpy as np

def find_thres(spectrogram,percentile,base):
    "Find the peak picking threshold for a particular spectrogram"
    dim = spectrogram.shape
    window = spectrogram[0:dim[0],base:dim[1]]
    threshold = np.percentile(window, percentile)

    return threshold

class peak:
    def __init__(self,t,f,S):
        self.time=t
        self.freq=f
        self.value=S[t,f]

def peak_pick (S,f_dim1,t_dim1,f_dim2,t_dim2,threshold,base):
    "Selects local peaks in a spectrogram and returns a list of tuples (time, freq, amplitude)"
    "S is spectrogram matrix"
    "f_dim1,f_dim2,t_dim1,and t_dim2 are freq x time dimensions of the sliding window for first and second passes"
    "threshold is the minimum amplitude required to be a peak"
    "base is the lowest frequency bin considered"

    a = len(S) #num of time bins
    b = len(S[1]) #num of frequency bins

    peaks = []
#    t_coords = []
#    f_coords = []

    "Determine the time x frequency window to analyze"
    "<=> adjust it to the borders of the spectrogram S"
    for i in range(0,a,t_dim1):
        for j in range(base,b,f_dim1):
            if i + t_dim1 < a and j + f_dim1 < b:
                window = S[i:i+t_dim1,j:j+f_dim1]
            elif i + t_dim1 < a and j + f_dim1 >= b:
                window = S[i:i+t_dim1,j:b]
            elif i + t_dim1 >= a and j + f_dim1 < b:
                window = S[i:a,j:j+f_dim1]
            else:
                window = S[i:a,j:b]

            "Check if the largest value in the window is greater than the threshold "
            "ie if there are peaks in it"
            if np.amax(window) >= threshold:
                row, col = np.unravel_index(np.argmax(window), window.shape)
                # pulls coordinates of max value from window
                p=peak(i+row,j+col,S)
                peaks.append(p)
#                t_coords.append(i+row)
#                f_coords.append(j+col)
#
    "Iterates through coordinates selected above to make sure that each of those points is in fact a local peak"

    for pk in peaks:
        fmin=pk.freq-f_dim2
        fmax=pk.freq+f_dim2
        tmin=pk.time-t_dim2
        tmax=pk.time+t_dim2
#    for k in range(0,len(f_coords)):
#        fmin = f_coords[k] - f_dim2
#        fmax = f_coords[k] + f_dim2
#        tmin = t_coords[k] - t_dim2
#        tmax = t_coords[k] + t_dim2
        if fmin < base:
            fmin = base
        if fmax > b:
            fmax = b
        if tmin < 0:
            tmin = 0
        if tmax > a:
            tmax = a
        window = S[tmin:tmax,fmin:fmax]
        #window centered around current coordinate pair

        "Break when the window is empty"
        if not window.size==0:
            continue

        "Eliminates coordinates that are not local peaks by setting their coordinates to -1"
        if S[pk.time,pk.freq] < np.amax(window):
            peaks.remove(pk)
#            t_coords[k] = -1
#            f_coords[k] = -1
#
#    "Removes all -1 coordinate pairs"
#    f_coords[:] = (value for value in f_coords if value != -1)
#    t_coords[:] = (value for value in t_coords if value != -1)
#
#    for x in range(0, len(peaks)):
#        peaks.append((t_coords[x], f_coords[x], S[t_coords[x], f_coords[x]]))

    return peaks
"categorize peaks, then remove those who don't satisfy the threshold criteria"
def reduce_peaks(peaks,fftsize,threshold):

    #Separate regions ensure better spread of peaks.
    low_peaks = []
    high_peaks = []

    for item in peaks:
        "pourquoi ce critere de fftsize/4?"
        if(item.freq>(fftsize/4)):
            high_peaks.append(item)
        else:
            low_peaks.append(item)

    reduced_peaks = []
    for item in peaks:
#       
#    the very low sound band (from bin 0 to 10)
#the low sound band (from bin 10 to 20)
#the low-mid sound band (from bin 20 to 40)
#the mid sound band (from bin 40 to 80)
#the mid-high sound band (from bin 80 to 160)
#the high sound band (from bin 160 to 511)
        [vlpeaks,lpeaks,lmpeaks,mpeaks,mhpeaks,hpeaks]=[]*6
        bands=[vlpeaks,lpeaks,lmpeaks,mpeaks,mhpeaks,hpeaks]
        if (item.freq<fftsize*10/512):
            vlpeaks.append(item)
        elif (item.freq<fftsize*20/512):
            lpeaks.append(item)
        elif (item.freq<fftsize*40/512):
            lmpeaks.append(item)
        elif (item.freq<fftsize*80/512):
            mpeaks.append(item)
        elif (item.freq<fftsize*160/512):
            mhpeaks.append(item)
        else:
            hpeaks.append(item)
        
        #get the 6 strongest bins 
        reduced_peaks=[]
        for band in bands:
            reduced_peaks.append(np.argmax([pk.value for pk in band]))
            
        #compute an average of the values and keep only the ones above the threshold
        moy=np.mean([pk.value for pk in reduced_peaks])
        for pk in reduced_peaks:
            if (pk.value<moy*threshold):
                reduced_peaks.remove(pk)
                
         #if(item.freq>(fftsize/4)):
#            if(item.value>np.percentile([pk.freq for pk in high_peaks],high_peak_threshold,axis=0)):
#                reduced_peaks.append(item)
#            else:
#                continue
#        else:
#            if(item.value>np.percentile([pk.freq for pk in low_peaks],low_peak_threshold,axis=0)):
#                reduced_peaks.append(item)
#            else:
#                continue
    ###############################################################
        
    return reduced_peaks