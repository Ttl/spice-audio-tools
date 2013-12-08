import sys, wave, struct
SAMPLING_RATE = 44100

def parse_output(output):
    value={}
    output=output.split('\n')
    index=1
    current = ()
    for line in xrange(len(output)):
        temp=output[line].replace(',','').split()
        if len(temp)>0:
            if temp[0]=='Index':
                if line+2<len(output):
                    temp2=output[line+2].replace(',','').split()
                    if float(temp2[0])<index:
                        current = temp[2]
                        value[temp[2]]=([],[])
                        index=0

        if len(temp)>2 and current!=():
            try:
                float(temp[1]),float(temp[2])
            except:
                continue
            index+=1
            value[current][0].append(float(temp[1]))
            value[current][1].append(float(temp[2]))
    return value

def lin_interp(x0,x1,y0,y1,x):
    x0 = float(x0)
    x1 = float(x1)
    y0 = float(y0)
    y1 = float(y1)
    x = float(x)
    return y0+(x-x0)*(y1-y0)/(x1-x0)

def write_wav(data,filename):
    w = wave.open(filename,'w')
    k = data[data.keys()[0]]
    w.setparams((1, 2, SAMPLING_RATE, 0, 'NONE', 'not compressed'))
    m = max(max(k[1]),-min(k[1]))
    if clipping==False:
        vrange = m
    values = []
    t = 0.0
    step = 1.0/SAMPLING_RATE

    for i in xrange(len(k[1])-1):
        while k[0][i]<=t*step<k[0][i+1]:
            sample = lin_interp(k[0][i],k[0][i+1],k[1][i],k[1][i+1],t*step)/vrange
            sample = 1 if sample >1 else sample
            sample = -1 if sample <-1 else sample
            d = struct.pack('<h',int(32767*sample))
            values.append(d)
            t += 1

    w.writeframes(''.join(values))
    w.close()


if __name__ == "__main__":
    if len(sys.argv)<=2:
        print """Usage: spicetowav <file> <output> [clipping voltage, m = no clipping]
        Converts spice transient output to wav format."""
        exit()
    lines = ''.join(open(sys.argv[1]).readlines())
    clipping = False
    if len(sys.argv)>3:
        if sys.argv[3] != 'm':
            vrange = float(sys.argv[3])
            clipping = True
    write_wav(parse_output(lines),sys.argv[2])
