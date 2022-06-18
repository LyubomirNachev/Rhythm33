from logging import logProcesses
import os
import random
from textwrap import shorten
import time
from turtle import position
import kivy
from pytube import YouTube
import subprocess
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider


Window.size = (400, 600)
global song_number
song_number = 0
global seconds_elapsed
seconds_elapsed=0
global loop_control
loop_control=False
global shuffle_control
shuffle_control=False

global Flag_stop_manual
Flag_stop_manual = False

class MusicApp(MDApp):
    def build(self):

        layout = MDRelativeLayout(md_bg_color = [50/255, 112/255, 175/255, 1])

        self.music_dir = "C:/Users/Misho/Documents/daskalo/Programirane 11 klas/proekt/Rhythm33-main"

        self.music_files = os.listdir(self.music_dir)

        print(self.music_files)

        self.song_list = [x for x in self.music_files if x.endswith(('mp3'))]

        self.song_count = len(self.song_list)

        self.dtext = Label(pos_hint = {'center_x':0.13, 'center_y':0.95},
                           size_hint = (1,1),
                           font_size = (18),
                           text = "Download: ")

        self.submit = MDIconButton(pos_hint={'center_x':0.9,'center_y':0.95},
                                    icon = 'enter.png',
                                    on_press=self.enter)

        self.download = TextInput(pos_hint={'center_x':0.53, 'center_y':0.95},
                                  multiline=False,
                                  size_hint_y = None,
                                  height = 30,
                                  size_hint_x = None,
                                  width = 220)

        self.songLabel = Label(pos_hint={'center_x':0.5, 'center_y':0.66},
                               size_hint = (200,135),
                               font_size = 15,
                               text_size = (200,135),
                               halign = 'center',
                            #    shorten = True,
                              split_str = "_"
                            )

        self.songImage = Image(pos_hint = {'center_x':0.5, 'center_y':0.35},
                               size_hint = (0.40, 0.27))

        self.currenttime = Label(text = "00:00",
                                 pos_hint={'center_x':.16, 'center_y':.145},
                                 size_hint=(1,1),
                                 font_size=18)

        self.totaltime = Label(text = "00:00",
                                 pos_hint={'center_x':.84, 'center_y':.145},
                                 size_hint=(1,1),
                                 font_size=18)

        self.progressbar = ProgressBar(max = 100,
                                       value =0,
                                       pos_hint = {'center_x':0.5,'center_y':0.12},
                                       size_hint = (.8,.75),)

        self.slider = Slider(min=0,
                             max=1,
                             step=0.1,
                             orientation = 'vertical',
                             value = 1,
                             pos_hint = {'center_x':0.1,'center_y':0.5},
                             size_hint = (.1,.5),
                             on_touch_move =self.vol,
                             on_touch_up = self.vol)

        self.playbutton = MDIconButton(pos_hint={'center_x':0.425,'center_y':0.05},
                                       icon = 'play.png',
                                       on_press = self.playaudio)

        self.stopbutton = MDIconButton(pos_hint={'center_x':0.575,'center_y':0.05},
                                       icon = 'stop.png',
                                       on_press = self.stopaudio)

        self.nextbutton = MDIconButton(pos_hint={'center_x':0.725,'center_y':0.05},
                                       icon = 'next.png',
                                       on_press = self.nextsong)

        self.prevbutton = MDIconButton(pos_hint={'center_x': 0.275, 'center_y': 0.05},
                                       icon='prev.png',
                                       on_press = self.prevsong)

        self.shufflebutton = MDIconButton(pos_hint={'center_x': 0.890, 'center_y': 0.05},
                                          icon='shuffle.png',
                                          on_press = self.shuffle)

        self.loopbutton = MDIconButton(pos_hint={'center_x': 0.1, 'center_y': 0.05},
                                       icon='loop.png',
                                       on_press = self.loop)

        layout.add_widget(self.slider)
        layout.add_widget(self.playbutton)
        layout.add_widget(self.stopbutton)
        layout.add_widget(self.songLabel)
        layout.add_widget(self.songImage)
        layout.add_widget(self.progressbar)
        layout.add_widget(self.currenttime)
        layout.add_widget(self.totaltime)
        layout.add_widget(self.nextbutton)
        layout.add_widget(self.prevbutton)
        layout.add_widget(self.shufflebutton)
        layout.add_widget(self.loopbutton)
        layout.add_widget(self.download)
        layout.add_widget(self.dtext)
        layout.add_widget(self.submit)

        self.song_title = self.song_list[song_number]
        self.songLabel.text = "=== Stopped ==="
        Clock.schedule_once(self.song_load)


        return layout

    def song_load(self, obj):

        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir,self.song_title))
        self.songImage.source = "background.png"
        self.sound.on_stop = self.song_end
        self.sound.volume = self.slider.value

    def vol(self, touch, obj):
        self.sound.volume = self.slider.value

    def playaudio(self, obj):

        self.songLabel.text = "=== Playing: " + self.song_title[0:-4] + " ==="
        global Flag_stop_manual
        Flag_stop_manual = True

        self.sound.play()
        Flag_stop_manual = False

        self.progressbar.value = 0
        global seconds_elapsed
        seconds_elapsed = 0
        self.currenttime.text = "00:00"
        total_time = time.strftime('%M:%S', time.gmtime(self.sound.length))
        self.totaltime.text = total_time
        self.progressbarEvent = Clock.schedule_interval(self.updatepbar,self.sound.length/100)
        self.setttimeEvent = Clock.schedule_interval(self.settime,0.5)

    def stopaudio(self, obj):

        global Flag_stop_manual
        Flag_stop_manual = True

        self.sound.stop()
        Flag_stop_manual = False
        self.songLabel.text = "=== Stopped ==="
        


    def nextsong(self, obj):

        global Flag_stop_manual
        Flag_stop_manual = True

        is_playing=self.sound.state=="play"
        self.sound.stop()
        Flag_stop_manual = False
        global song_number
        song_number = song_number + 1

        if song_number == self.song_count:
            song_number = 0
        self.song_title = self.song_list[song_number]
        self.song_load(obj)
        if(is_playing==True):
            self.playaudio(obj)

    def prevsong(self, obj):

        global Flag_stop_manual
        Flag_stop_manual = True
        is_playing=self.sound.state=="play"
        self.sound.stop()
        Flag_stop_manual = False
        
        global song_number
        song_number = song_number - 1
        if song_number == -1:
            song_number = self.song_count - 1
        self.song_title = self.song_list[song_number]
        self.song_load(obj)

        if(is_playing==True):
            self.playaudio(obj)

    def shuffle(self, obj):

        global shuffle_control
        shuffle_control= not shuffle_control

    def loop(self, obj):

        global loop_control
        loop_control= not loop_control


    def song_end(self):

        self.progressbarEvent.cancel()
        self.setttimeEvent.cancel()
        self.progressbar.value = 0
        global seconds_elapsed
        seconds_elapsed = 0
        self.currenttime.text = "00:00"
        self.totaltime.text = "00:00"

        print("POOTIS")
        global Flag_stop_manual
        if(Flag_stop_manual == True):
            Flag_stop_manual = False
            return

        global loop_control
        if(loop_control==True):
            self.playaudio(self)
            return

        global shuffle_control
        global song_number
        if(shuffle_control==True):
            song_number = random.randint(0, self.song_count-1)
        else:
            song_number = song_number + 1
            if song_number == self.song_count:
                song_number = song_number - 1
                self.songLabel.text = "=== Stopped ==="
                return
        self.song_title = self.song_list[song_number]
        self.song_load(self)
        self.playaudio(self)






    def enter(self, obj):
        download = self.download.text

        url = download
        try:
            yt = YouTube(url)
        except:
            print("YOU FUCKING IDIOT enter a fucking ")
            return

        name = yt.title.replace(' ', '_')
        only_audio_streams = (yt.streams.filter(only_audio=True))
        destination = "\"" + self.music_dir + "/"
        stream = yt.streams.get_audio_only('mp4')
        stream.download(filename = name + '.mp4')
        mp4 = name + '.mp4'
        mp3 = destination + name + '.mp3\"'
        ffmpeg = ('ffmpeg -i %s ' % mp4 + mp3)
        subprocess.call(ffmpeg, shell=True)
        os.remove(name + '.mp4')
        self.download.text = " "

        music_files_new = os.listdir(self.music_dir)
        song_list_new = [x for x in music_files_new if x.endswith(('mp3')) and x not in self.song_list]
        for x in song_list_new:
            self.song_list.append(x)
        self.song_count = len(self.song_list)

    def updatepbar(self, value):
        if self.progressbar.value < 100:
            self.progressbar.value +=1
    def settime(self, t):
        global seconds_elapsed
        current_time = time.strftime('%M:%S', time.gmtime(seconds_elapsed))
        self.currenttime.text = current_time
        seconds_elapsed = seconds_elapsed + t

if __name__ == '__main__':
	MusicApp().run()