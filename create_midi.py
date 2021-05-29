import mido
from mido import Message,MidiFile,MidiTrack
import sys

def transfer(statics,g,s):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', channel=0, program=2, time=0))
    for i in statics:
        for j in i:
            a=j[0]*240
            num=j[1]
            if num<=3:
                d=58+2*num
            elif 4<=num<=7:
                d=58+2*num-1
            elif 8<=num<=10:
                d=58+2*num-2
            elif 11<=num:
                d=58+2*num-3
            track.append(Message('note_on', note=d, velocity=64, time=0, channel=0))
            track.append(Message('note_off', note=d, velocity=64, time=a, channel=0))
    mid.save(f'第{g}代第{s}段.mid')
    return
