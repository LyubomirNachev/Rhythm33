from pytube import YouTube
import subprocess
import os
url = input("What is the url:")
yt = YouTube(url)
name = yt.title.replace(' ', '_')
only_audio_streams =(yt.streams.filter(only_audio=True))
destination = "C:/Users/lubol/OneDrive/Desktop"
#for i in only_audio_streams:
#for i in only_audio_streams:
#    print(only_audio_streams)
#    print('')
stream = yt.streams.get_audio_only('mp4')
stream.download(filename=name + '.mp4')
mp4 = name + '.mp4'
mp3 = name + '.mp3'
ffmpeg = ('ffmpeg -i %s ' % mp4 + mp3)
subprocess.call(ffmpeg, shell=True)
os.remove(name + '.mp4')
