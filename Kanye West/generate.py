import numpy as np
import tensorflow as tf
from tensorflow import keras
import sys
import os

tf.get_logger().setLevel('ERROR')

def restore_model():
    # Either restore the latest model, or create a fresh one
    # if there is no checkpoint available.
    checkpoint_dir = './ckpt'
    checkpoints = [checkpoint_dir + '/' + name
                   for name in os.listdir(checkpoint_dir)]
    if checkpoints:
        latest_checkpoint = max(checkpoints, key=os.path.getctime)
        print('Restoring from', latest_checkpoint)
        return keras.models.load_model(latest_checkpoint)


tokenizer = keras.preprocessing.text.Tokenizer(char_level=True)
with open("KanyeWest.txt") as f:
    text = f.read()
    tokenizer.fit_on_texts(text)
    max_id = len(tokenizer.word_index)

model = restore_model()

def preprocess(texts):
    X = np.array(tokenizer.texts_to_sequences(texts)) - 1
    return tf.one_hot(X, max_id)

def next_char(text, temperature=1):
    X_new = preprocess([text])
    y_prob = model.predict(X_new)[0,-1:,:]
    rescaled = tf.math.log(y_prob)/temperature
    char_id = tf.random.categorical(rescaled, num_samples=1) + 1
    return tokenizer.sequences_to_texts(char_id.numpy())[0]

def complete_text(text, n_chars=50, temperature=1):
    for _ in range(n_chars):
        text+=next_char(text, temperature)
        print(text)
    for i in range(10):
        print()
    return text

if __name__ == "__main__":
    argv_size = len(sys.argv)
    start = 'i'
    num = 100
    temp = 0.6
    if argv_size>1 and sys.argv[1]=='help':
        print("usage: [letter] [num chars] [temperature]")
    elif argv_size>1:
        start = sys.argv[1]
    if argv_size>2:
        num = int(sys.argv[2])
    if argv_size>3:
        temp = float(sys.argv[3])
    print(complete_text(start, n_chars=num, temperature=temp))