# -*- coding: utf-8 -*-
"""Text Generation for Local Runtime

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13qFdpdYCC2hRWg9r3Opr6YtTb9J2aLm_
"""

# imports
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.utils import np_utils

# open data (filename may vary, be wary)
text=(open("HarryPotterBookOne.txt").read())
text=text.lower()

# assign characters to numbers for better training
characters = sorted(list(set(text)))
numToChar = {n:char for n, char in enumerate(characters)}
charToNum = {char:n for n, char in enumerate(characters)}

# adjusting data prior to training
X = [] # train
Y = [] # "target"
length = len(text)
seq_length = 100 # number of characters to consider before predicting a character
for i in range(0, length-seq_length, 1):
    sequence = text[i:i + seq_length]
    label = text[i + seq_length]
    X.append([charToNum[char] for char in sequence])
    Y.append(charToNum[label])
    
# modifying datasets
X_modified = np.reshape(X, (len(X), seq_length, 1))
X_modified = X_modified / float(len(characters))
Y_modified = np_utils.to_categorical(Y)

# training :)
model = Sequential()
model.add(LSTM(400, input_shape=(X_modified.shape[1], X_modified.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(400, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(400))
model.add(Dropout(0.2))
model.add(Dense(Y_modified.shape[1], activation="softmax"))
model.compile(loss="categorical_crossentropy", optimizer="adam")

# loading weights
model.load_weights("weights.h5")

# generating :)
string_mapped = X[99]
full_string = [numToChar[value] for value in string_mapped]
for i in range (2048):
    x = np.reshape(string_mapped, (1, len(string_mapped), 1))
    x = x / float(len(characters))
    pred_index = np.argmax(model.predict(x, verbose=0))
    seq = [numToChar[value] for value in string_mapped]
    full_string.append(numToChar[pred_index])
    string_mapped.append(pred_index)
    string_mapped = string_mapped[1:len(string_mapped)]
    
# output
text = ""
for char in full_string:
    text = text+char

text_file = open("generated.txt", "w")
n = text_file.write(text)
text_file.close()
