import os
import wavio
import numpy
pitches=["A3","D4","A4","D5"]

with open("_VC\\oto.ini") as otofile:
    lines=otofile.readlines()

otodict={}#(wav文件名，音高)->对应的oto条目、
for line in lines:
    linecontent=line.replace("=",",").split(",")
    for i in [2,3,4,5,6]:
        linecontent[i]=float(linecontent[i])
    otodict[(linecontent[0],linecontent[1][-2:])]=otodict.get((linecontent[0],linecontent[1][-2:]),[])+[linecontent]

def minstarttime(otolist):
    return min([oto[2]] for oto in otolist)[0]

def maxendtime(otolist):
    return max([oto[2]-oto[4]] for oto in otolist)[0]

outputoto=[[],[],[],[]]
for filename in os.listdir("_VC"):
    if(filename.endswith(".wav")):
        starttimes=numpy.array([minstarttime(otodict[(filename,pitch)]) for pitch in pitches])
        endtimes=numpy.array([maxendtime(otodict[(filename,pitch)]) for pitch in pitches])
        offsets=numpy.array([0,0,0,0])
        if(filename.endswith("_bre1.wav")):
            offsets[1:]=endtimes[:-1]+100
            wav=wavio.read(os.path.join("_VC",filename))
            wavio.write(os.path.join("A3",filename),wav.data[0:splitpoints[1]],rate=44100, sampwidth=1)
            wavio.write(os.path.join("D4",filename),wav.data[splitpoints[1]:splitpoints[2]],rate=44100, sampwidth=1)
            wavio.write(os.path.join("A4",filename),wav.data[splitpoints[2]:splitpoints[3]],rate=44100, sampwidth=1)
            wavio.write(os.path.join("D5",filename),wav.data[splitpoints[3]:],rate=44100, sampwidth=1)
        else:
            offsets[1:]=(endtimes[:-1]+starttimes[1:]*2)/3
        splitpoints=(offsets*44100/1000).astype(int)
        print(filename,endtimes)
        #音频切割
        #wav=wavio.read(os.path.join("_VC",filename))
        #wavio.write(os.path.join("A3",filename),wav.data[0:splitpoints[1]],rate=44100, sampwidth=1)
        #wavio.write(os.path.join("D4",filename),wav.data[splitpoints[1]:splitpoints[2]],rate=44100, sampwidth=1)
        #wavio.write(os.path.join("A4",filename),wav.data[splitpoints[2]:splitpoints[3]],rate=44100, sampwidth=1)
        #wavio.write(os.path.join("D5",filename),wav.data[splitpoints[3]:],rate=44100, sampwidth=1)
        #oto转换
        for i in [0,1,2,3]:
            otos=otodict[(filename,pitches[i])]
            for oto in otos:
                oto[2]-=offsets[i]
            outputoto[i]+=otos
for i in [0,1,2,3]:
    with open(os.path.join(pitches[i],"oto.ini"),"w") as otofile:
        otofile.write("\n".join(["{}={},{},{},{},{},{}".format(*oto) for oto in outputoto[i]]))
