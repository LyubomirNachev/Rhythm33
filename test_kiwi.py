import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from pytube import YouTube
from kivy.properties import ObjectProperty
import subprocess
import os

class MyGridLayout(Widget):

	name = ObjectProperty(None)
	download = ObjectProperty(None)

	def press(self):
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
		#self.add_widget(Label(text=f'Finished Download!'))


		# Clear the input boxes
		self.download.text = ""

class MyApp(App):
	def build(self):
		return MyGridLayout()


if __name__ == '__main__':
	MyApp().run()
