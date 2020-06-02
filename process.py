import json
import sys

with open(sys.argv[1]) as json_file:
    data = json.load(json_file)

name = sys.argv[1]
idx1 = name.index('_')
name = name[idx1+1:-5]
name += ".txt"

f = open(name, "w+")

no_lyrics = "Lyrics for this song have yet to be released. Please check back once the song has been released."
songs = data['songs']
for song in songs:
    # print(song['lyrics'])
    # print()
    s = song['lyrics']
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        pass
    else:
        if no_lyrics in s:
            pass
        else:
            f.write(s)
            f.write("\n\n")

    