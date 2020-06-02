import os
import sys
import tensorflow as tf
from tensorflow import keras
import prep_dataset

# Prepare a directory to store all the checkpoints.
checkpoint_dir = './ckpt'
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)


def make_model(max_id):
    # Create a new linear regression model.
    model = keras.models.Sequential([
    keras.layers.GRU(128, return_sequences=True, input_shape=[None, max_id],
                     dropout=0.2, recurrent_dropout=0.2),
    keras.layers.GRU(128, return_sequences=True,
                     dropout=0.2, recurrent_dropout=0.2),
    keras.layers.TimeDistributed(keras.layers.Dense(max_id,
                                                    activation="softmax"))
])
    model.compile(loss="sparse_categorical_crossentropy", optimizer="adam")
    return model


def make_or_restore_model(max_id):
    # Either restore the latest model, or create a fresh one
    # if there is no checkpoint available.
    checkpoints = [checkpoint_dir + '/' + name
                   for name in os.listdir(checkpoint_dir)]
    if checkpoints:
        latest_checkpoint = max(checkpoints, key=os.path.getctime)
        print('Restoring from', latest_checkpoint)
        return keras.models.load_model(latest_checkpoint)
    print('Creating a new model')
    return make_model(max_id)


dataset, max_id, train_size, batch_size = prep_dataset.get_dataset(sys.argv[1])
dataset = dataset.prefetch(1)

model = make_or_restore_model(max_id)
callbacks = [
    # This callback saves a SavedModel every 100 batches.
    # We include the training loss in the folder name.
    keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_dir + '/ckpt-loss={loss:.2f}',
        save_freq=300)
]
model.fit(dataset, steps_per_epoch=train_size // batch_size,
                    epochs=10, callbacks=callbacks)