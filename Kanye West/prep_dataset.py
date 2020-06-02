import sys
import sklearn
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
import pickle

def get_dataset(filename, batch_size=32):
    #filename = sys.argv[1]
    with open(filename) as f:
        file_text = f.read()

    tokenizer = keras.preprocessing.text.Tokenizer(char_level=True)
    tokenizer.fit_on_texts(file_text)

    max_id = len(tokenizer.word_index)
    dataset_size = tokenizer.document_count

    [encoded] = np.array(tokenizer.texts_to_sequences([file_text])) - 1
    train_size = dataset_size * 90 // 100
    dataset = tf.data.Dataset.from_tensor_slices(encoded[:train_size])

    n_steps = 100
    window_length = n_steps + 1
    dataset = dataset.repeat().window(window_length, shift=1, drop_remainder=True)

    dataset = dataset.flat_map(lambda window: window.batch(window_length))

    dataset = dataset.shuffle(10000).batch(batch_size)
    dataset = dataset.map(lambda windows: (windows[:,:-1], windows[:,1:]))

    dataset = dataset.map(lambda X_batch, Y_batch: (tf.one_hot(X_batch, depth=max_id), Y_batch))

    return dataset, max_id, train_size, batch_size