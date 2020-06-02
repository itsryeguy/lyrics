import lyricsgenius
import config
import sys
import os

api = lyricsgenius.Genius(config.client_token)
artist_name = sys.argv[1]
song_count = -1
if len(sys.argv) > 2:
    song_count = int(sys.argv[2])

try:
    if(song_count != -1):
        artist = api.search_artist(artist_name,max_songs=song_count)
    else:
        artist =  api.search_artist(artist_name)
finally:
    new_dir = './'+artist_name
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    os.chdir(new_dir)
    artist.save_lyrics()
