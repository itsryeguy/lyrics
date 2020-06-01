import lyricsgenius
import config
import sys

api = lyricsgenius.Genius(config.client_token)
artist_name = sys.argv[1]
try:
    artist =  api.search_artist(artist_name)
finally:
    artist.save_lyrics()
