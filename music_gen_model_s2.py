# -*- coding: utf-8 -*-
"""music-gen_model_s2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JajkYX2tgqr2TlwsyPnFqynKXWUYGoyX

# Music Generation using LSTM model

## Creating the model
"""

print("Re-running required files............")
# Importing librries
import glob
import numpy as np
import tensorflow as tf
from music21 import converter, instrument, note, chord        # music21 is used to interpret musical notes and data
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical

# Function to create the LSTM model
"""def create_lstm_model(input_shape, output_shape):
    model = Sequential()
    model.add(LSTM(256, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512))
    model.add(Dropout(0.3))
    model.add(Dense(output_shape, activation='softmax'))
    return model"""

# Function to preprocess the MIDI data
def preprocess_data(file_path):
    notes = []
    midi = converter.parse(file_path)
    notes_to_parse = None
    parts = instrument.partitionByInstrument(midi)
    if parts:  # File has instrument parts
        notes_to_parse = parts.parts[0].recurse()
    else:  # File has notes in a flat structure
        notes_to_parse = midi.flat.notes
    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))
    return notes

# Function to generate input and output sequences
def generate_sequences(notes, sequence_length):
    input_sequences = []
    output_sequences = []
    for i in range(len(notes) - sequence_length):
        input_sequence = notes[i:i + sequence_length]
        output_sequence = notes[i + sequence_length]
        input_sequences.append(input_sequence)
        output_sequences.append(output_sequence)
    return input_sequences, output_sequences

# Mounting the Drive
#from google.colab import drive
#drive.mount('/content/drive')

# Loading and preprocessing the MIDI files

midi_files = glob.glob("/midi_songs/*.mid")
notes = []
for file in midi_files:
  notes += preprocess_data(file)

# Checking if any MIDI files were found
if len(notes) == 0:                         # then attach a random pseudo examples
    print("No notes generated files appear to corrupted adding pseudo examples")
    notes=['F4', 'F2', 'F4', 'G4', '0.3.5', 'A4', '0.3.5', 'B-4', 'B-2', 'C5', 'D5', '10.2.5', 'E-5', 'B-2', 'F5', 'G5', '3', 'A5', '3.7.10', '10.0', '10.0', '10.0', '10.0', 'A5', 'G5', '5.10', 'B-2', 'B-5', 'D5', '10.2.5', '10.2.5', '3.7', 'F2', 'G5', 'A4', '0.3.5', '0.3.5', '10.2', 'B-2', 'D5', 'E4', '10.2.5', '10.2.5', 'F4', 'F2', 'A4', 'C5', '3.5', 'E-5', 'G5']
else:
    print("Scanned midi files..............")

# Creating a vocabulary of unique notes
print("Printing unique notes..............")
unique_notes = sorted(set(notes))
num_unique_notes = len(unique_notes)
print(unique_notes)

# Creating input and output sequences
sequence_length = 10 # Adjust the sequence length as per your preference
input_sequences, output_sequences = generate_sequences(notes, sequence_length)

# Converting input and output sequences to numeric format
note_to_int = dict((note, number) for number, note in enumerate(unique_notes))
input_sequences_numeric = []
output_sequences_numeric = []
for input_seq, output_seq in zip(input_sequences, output_sequences):
    input_sequences_numeric.append([note_to_int[note] for note in input_seq])
    output_sequences_numeric.append(note_to_int[output_seq])
print(input_sequences_numeric)

# Checking if input sequences are empty
if len(input_sequences_numeric) == 0:
    print("No input sequences found. Please check your MIDI files or adjust the sequence length.")

# Converting input and output sequences to numpy arrays
input_sequences_numeric = np.array(input_sequences_numeric)
output_sequences_numeric = np.array(output_sequences_numeric)

# Defining the input and output shapes for the LSTM model
input_shape = (sequence_length, num_unique_notes)  # Replace with your desired values
output_shape = num_unique_notes  # Replace with your desired number of unique notes

# Normalizing input sequences
input_sequences_normalized = input_sequences_numeric / float(num_unique_notes)

"""## Training using Distributed Training"""

from tensorflow.keras.callbacks import ModelCheckpoint, Callback
from tensorflow.keras.utils import to_categorical
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

print('Successfully loaded previous files')
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical

# Load the model saved from Host 1
print("Loading host1 model/............")
model = load_model('model.h5')

# Custom callback to collect training speed and convergence per epoch
class TrainingStatsCallback(Callback):
    def __init__(self):
        self.start_time = 0
        self.steps = 0
        self.speeds = []
        self.convergences = []

    def on_train_begin(self, logs=None):
        self.start_time = time.time()

    def on_train_batch_end(self, batch, logs=None):
        self.steps += 1

    def on_epoch_end(self, epoch, logs=None):
        if logs is not None:
            epoch_time = time.time() - self.start_time
            speed = epoch_time / self.steps
            self.speeds.append(speed)
            self.convergences.append(logs.get('loss'))
            self.steps = 0

# Create the mirrored strategy
strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy(
    tf.distribute.experimental.CollectiveCommunication.RING
)

# Input reshape for LSTM layer
#input_shape = (sequence_length, 1)

# Reshaping input sequences
#input_sequences_normalized = np.expand_dims(input_sequences_normalized, axis=2)

# Define the model creation function inside the strategy scope
with strategy.scope():
    model = load_model('model.h5')
    model.compile(loss='categorical_crossentropy', optimizer=Adam())

# Define the training stats callback
stats_callback = TrainingStatsCallback()

print("Start training.......")
model.fit(input_sequences_normalized, to_categorical(output_sequences_numeric),
          epochs=1000, batch_size=64)

# Define the training stats callback
stats_callback = TrainingStatsCallback()

# Plot the training speed and convergence per epoch
epochs = range(1, len(stats_callback.speeds) + 1)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(epochs, stats_callback.speeds)
plt.xlabel('Epochs')
plt.ylabel('Training Speed (seconds/step)')
plt.title('Training Speed per Epoch')

plt.subplot(1, 2, 2)
plt.plot(epochs, stats_callback.convergences, 'r-o')
plt.xlabel('Epochs')
plt.ylabel('Convergence')
plt.title('Convergence per Epoch')

plt.tight_layout()
plt.show()
plt.savefig('pic2.png')
#import subprocess

# View the PNG image in the terminal using the 'feh' command
#image_path = 'pic2.png'
#subprocess.run(['feh', '-g', '800x600', image_path])


"""## Generation of Music"""

# Loading the best model for generating music
with strategy.scope():
    model = tf.keras.models.load_model('model.h5')

print('Generating music please wait..........')
# Generating music using the trained model
start_sequence = input_sequences_normalized[np.random.randint(0, len(input_sequences_normalized) - 1)]
generated_notes = []
for i in range(500):  # Adjust the number of notes to generate as per your preference
    input_sequence = np.reshape(start_sequence, (1, len(start_sequence), 1))
    prediction = model.predict(input_sequence, verbose=0)
    index = np.argmax(prediction)
    generated_note = unique_notes[index]
    generated_notes.append(generated_note)
    start_sequence = np.append(start_sequence, index / float(num_unique_notes))
    start_sequence = start_sequence[1:]

# Viewing the generated notes
print(generated_notes)