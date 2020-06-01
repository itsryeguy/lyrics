import json
import sys

with open(sys.argv[1]) as json_file:
    data = json.load(json_file)

name = sys.argv[1]
idx1 = name.index('_')
name = name[idx1+1:-5]
name += ".txt"

f = open(name, "w+")

songs = data['songs']
for song in songs:
    # print(song['lyrics'])
    # print()
    f.write(song['lyrics'])
    f.write("\n\n")

    