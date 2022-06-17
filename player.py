import os
import random
import time
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

Window.size = (400, 600)
global song_number
song_number = 0

class MusicApp(MDApp):
    def build(self):

        layout = MDRelativeLayout(md_bg_color = [50/255, 112/255, 175/255, 1])

        self.music_dir = "C:/Users/lubol/OneDrive/Desktop/Rythm33"

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

        self.songLabel = Label(pos_hint={'center_x':0.5, 'center_y':0.56},
                               size_hint = (1,1),
                               font_size = 18)

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

        self.playbutton = MDIconButton(pos_hint={'center_x':0.425,'center_y':0.05},
                                       icon = 'play.png',
                                       on_press = self.playaudio)

        self.stopbutton = MDIconButton(pos_hint={'center_x':0.575,'center_y':0.05},
                                       icon = 'stop.png',
                                       on_press = self.stopaudio, disabled = True)

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

        Clock.schedule_once(self.playaudio)


        return layout

    def playaudio(self, obj):
        self.playbutton.disabled = True
        self.stopbutton.disabled = False
        self.song_title = self.song_list[song_number]
        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir,self.song_title))

        self.songLabel.text = "=== Playing: " + self.song_title[0:-4] + " ==="
        self.songImage.source = "background.png"

        self.sound.play()
        self.progressbarEvent = Clock.schedule_interval(self.updatepbar,self.sound.length/100)
        self.setttimeEvent = Clock.schedule_interval(self.settime,1)
    def stopaudio(self, obj):
        self.playbutton.disabled = False
        self.stopbutton.disabled = True
        self.sound.stop()
        self.songLabel.text = "=== Stopped ==="
        self.progressbarEvent.cancel()
        self.setttimeEvent.cancel()
        self.progressbar.value = 0
        self.currenttime.text = "00:00"
        self.totaltime.text = "00:00"
        self.songImage.source = "pause.png"
    def nextsong(self, obj):
        self.sound.stop()
        global song_number
        song_number = song_number + 1
        if song_number == self.song_count:
            song_number = 0
        self.song_title = self.song_list[song_number]
        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir,self.song_title))

        self.songLabel.text = "=== Playing: " + self.song_title[0:-4] + " ==="
        self.songImage.source = "background.png"

        self.sound.play()
        self.progressbarEvent = Clock.schedule_interval(self.updatepbar,self.sound.length/100)
        self.setttimeEvent = Clock.schedule_interval(self.settime,1)
    def prevsong(self, obj):
        self.sound.stop()
        global song_number
        song_number = song_number - 1
        if song_number == -1:
            song_number = self.song_count - 1
        self.song_title = self.song_list[song_number]
        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir,self.song_title))

        self.songLabel.text = "=== Playing: " + self.song_title[0:-4] + " ==="
        self.songImage.source = "background.png"

        self.sound.play()
        self.progressbarEvent = Clock.schedule_interval(self.updatepbar,self.sound.length/100)
        self.setttimeEvent = Clock.schedule_interval(self.settime,1)
    def shuffle(self, obj):
        self.sound.stop()
        self.song_title = self.song_list[random.randrange(0, self.song_count)]
        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir, self.song_title))

        self.songLabel.text = "=== Playing: " + self.song_title[0:-4] + " ==="
        self.songImage.source = "background.png"

        self.sound.play()
        self.progressbarEvent = Clock.schedule_interval(self.updatepbar, self.sound.length / 100)
        self.setttimeEvent = Clock.schedule_interval(self.settime, 1)
    def loop(self, obj):
        pass
    def enter(self, obj):
        download = self.download.text

        url = download
        yt = YouTube(url)
        name = yt.title.replace(' ', '_')
        only_audio_streams = (yt.streams.filter(only_audio=True))
        destination = "C:/Users/lubol/OneDrive/Desktop"
        stream = yt.streams.get_audio_only('mp4')
        stream.download(filename=name + '.mp4')
        mp4 = name + '.mp4'
        mp3 = name + '.mp3'
        ffmpeg = ('ffmpeg -i %s ' % mp4 + mp3)
        subprocess.call(ffmpeg, shell=True)
        os.remove(name + '.mp4')
        self.download.text = " "
    def updatepbar(self, value):
        if self.progressbar.value < 100:
            self.progressbar.value +=1
    def settime(self, t):
        current_time = time.strftime('%M:%S', time.gmtime(self.progressbar.value*self.sound.length/100))
        total_time = time.strftime('%M:%S', time.gmtime(self.sound.length))
        self.currenttime.text = current_time
        self.totaltime.text = total_time

if __name__ == '__main__':
	MusicApp().run()