import os
from kivy.core.audio import SoundLoader
import time

music_dir = "M:\Judas Priest"
music_files = os.listdir(music_dir)

song_list = [x for x in music_files if x.endswith(('.mp3'))]
song_count = len(song_list)

def song_play():
	song_title = song_list[selected_song-1]
	sound = SoundLoader.load('{}/{}'.format(music_dir, song_title))

	sound.play()
	time.sleep(sound.length)

i = 0

for i in range (song_count):
	print (i+1, song_list[i])

print("Enter number from 1 to", song_count, "to play a song") 
selected_song = input()
selected_song = int(selected_song)
song_play()
