import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from pytube import YouTube
import subprocess
import os

class MyGridLayout(GridLayout):
	# Initialize infinite keywords
	def __init__(self, **kwargs):
		# Call grid layout constructor
		super(MyGridLayout, self).__init__(**kwargs)

		# Set columns
		self.cols = 2

		# Create a second gridlayout
		self.top_grid = GridLayout()
		self.top_grid.cols = 1

		# Add widgets
		self.top_grid.add_widget(Label(text="Download: ", font_size=16))
		# Add Input Box
		self.download = TextInput(multiline=False,
			size_hint_y=None,
			height=30,
			size_hint_x=None,
			width=900
			)
		self.top_grid.add_widget(self.download)

		#Add the new top_grid to our app
		self.add_widget(self.top_grid)


		# Create a Submit Button
		self.submit = Button(text="Enter",
			font_size=16,
			size_hint_y=None,
			height=50,
			size_hint_x=None,
			width=100
			)
		# Bind the button
		self.submit.bind(on_press=self.press)
		self.top_grid.add_widget(self.submit)

	def press(self, instance):
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
		self.add_widget(Label(text=f'Finished Download!'))


		# Clear the input boxes
		self.download.text = ""

class MyApp(App):
	def build(self):
		return MyGridLayout()


if __name__ == '__main__':
	MyApp().run()
