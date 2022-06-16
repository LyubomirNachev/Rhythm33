import os
import random
import time
import kivy
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

Window.size = (400, 600)

class MusicApp(MDApp):
    def build(self):

        layout = MDRelativeLayout(md_bg_color = [50/255, 112/255, 175/255, 1])

        self.music_dir = "C:/Users/lubol/OneDrive/Desktop/Rythm33"

        self.music_files = os.listdir(self.music_dir)

        print(self.music_files)

        self.song_list = [x for x in self.music_files if x.endswith(('mp3'))]

        self.song_count = len(self.song_list)

        self.songLabel = Label(pos_hint={'center_x':0.5, 'center_y':0.96},
                               size_hint = (1,1),
                               font_size = 18)

        self.songImage = Image(pos_hint = {'center_x':0.5, 'center_y':0.55},
                               size_hint = (0.8,0.75))

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
                                       size_hint = (.8,.75))

        self.playbutton = MDIconButton(pos_hint={'center_x':0.4,'center_y':0.05},
                                       icon = 'play.png',
                                       on_press = self.playaudio)

        self.stopbutton = MDIconButton(pos_hint={'center_x':0.55,'center_y':0.05},
                                       icon = 'stop.png',
                                       on_press = self.stopaudio, disabled = True)

        layout.add_widget(self.playbutton)
        layout.add_widget(self.stopbutton)
        layout.add_widget(self.songLabel)
        layout.add_widget(self.songImage)
        layout.add_widget(self.progressbar)
        layout.add_widget(self.currenttime)
        layout.add_widget(self.totaltime)

        Clock.schedule_once(self.playaudio)

        return layout

    def playaudio(self, obj):
        self.playbutton.disabled = True
        self.stopbutton.disabled = False
        self.song_title = self.song_list[random.randrange(0, self.song_count)]
        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir,self.song_title))

        self.songLabel.text = "=== Playing: " + self.song_title[0:-4] + " ==="
        self.songImage.source = "1.jpg"

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