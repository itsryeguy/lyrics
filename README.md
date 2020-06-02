# Using a Char-RNN to generate lyrics based on data pulled from Genius.

### Setup

```python get_artist.py artist_name [song_num]```

searches for the artist and pulls as song_num number of songs worth of data, or as many as possible with valid data

```python process.py Lyrics_artist_name.json```

appends all the lyrics from the artist into a txt file.

### Training

copy train.py and prep_dataset.py into the folder you wish and run ```python train.py text_file_here```
