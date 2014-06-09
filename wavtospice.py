#Converts wav file to ngspice filesrc
import sys, wave, struct
from math import sqrt

def read_wav(filename):
    waveFile = wave.open(filename, 'r')
    data = []

    (nchannels, sampwidth, framerate, nframes, comptype, compname) = waveFile.getparams()
    timestep = 1.0/framerate
    print 'Framerate:',framerate
    print 'Sample width:', sampwidth
    t = 0
    print 'Channels:',nchannels
    for j in range(nframes):
        waveData = waveFile.readframes(1)
        #Take only the first channel
        waveData = waveData[:sampwidth]
        if sampwidth==1:
            temp = struct.unpack_from("<b", waveData)
        elif sampwidth==2:
            temp = struct.unpack_from("<h", waveData)
        elif sampwidth==3:
            temp = struct.unpack_from("<i", waveData+'\x00')
        elif sampwidth==4:
            temp = struct.unpack_from("<i", waveData)
        else:
            raise ValueError('Unsupported sample width')
        data.append((t*timestep,float(temp[0])/(2**(8*sampwidth)-1)))
        t += 1
    vrms = sqrt(1.0/(len(data[1]))*sum(i**2 for i in data[1]))
    print 'RMS voltage:',vrms
    return data


def write_spice(data,filename):
    with open(filename,'w') as f:
        [f.write("{:.6e} {:.4f}\n".format(*d)) for d in data]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print """Usage: wavtospice <.wav file> <spice input file>.
        Converts .wav to xspice filesource format."""
        exit()
    write_spice(read_wav(sys.argv[1]),sys.argv[2])
