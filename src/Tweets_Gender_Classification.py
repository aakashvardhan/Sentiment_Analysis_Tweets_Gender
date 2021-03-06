# -*- coding: utf-8 -*-
"""NN_final_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13sOehYMIGelDVbv7EDN5mYZZyRmV8vYw
"""

8 pip install tweet-preprocessor

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn import model_selection
from sklearn import metrics
from keras.preprocessing import sequence
from keras import layers
from keras.models import Sequential
from pandas import read_csv
import preprocessor as p #for tweet cleaning
from string import punctuation #for tweet cleaning
from collections import Counter #for dictionary building
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from sklearn.preprocessing import OrdinalEncoder,OneHotEncoder
from sklearn.preprocessing import LabelEncoder

np.random.seed(10000000)

df = pd.read_csv('/content/drive/My Drive/gender-classifier-DFE-791531 2.csv',encoding='latin1')
df.head()

df.fillna('missing',inplace=True)
df.head()

def clean_tweets(dataset):

    """
    clean_tweets removes URLS, punctuation, emojis and other
    symbols in tweets that are not words.
    """

    print("Started cleaning up tweets! This may take a few minutes.")

    new_dataset = []
    for tweet in dataset:
        #send to tweet_processor
        clean_tweet = p.clean(tweet)
        #remove puctuation
        for c in punctuation:
            clean_tweet = clean_tweet.replace(c,"")
        new_dataset.append(clean_tweet)

    print("Finished cleaning up tweets!")

    return new_dataset



def bag_of_words(dataset):

    """
    word_counter tallies all words used and encodes the tweets.
    """

    print("Starting to build dictionary! This may take a few minutes.")

    all_words = []

    for tweet in dataset:
        words = tweet.split()
        all_words = all_words + words

    count_words = Counter(all_words)
    total_words = len(count_words)
    sorted_words = count_words.most_common(total_words)
    vocab_to_int = {num:i+1 for i, (num,word) in enumerate(sorted_words)}
    print(vocab_to_int)
    print(len(vocab_to_int))
    print("Dictionary complete!")

    print("Encoding tweets based on dictionary! This may take a while.")
    new_dataset = []
    for tweet in dataset:
        enumerated = [vocab_to_int[word] for word in tweet.split()]
        new_dataset.append(enumerated)
    print("Tweets encoded! Your dataset is ready.")

    return new_dataset

x = df['text'].values
# bag_of_words(x)
maxlen = 280
max_features = 66849

print(x)

y = df['gender'].values   
print(y)

x = bag_of_words(clean_tweets(x))

print(x)

y = y.reshape((len(y), 1))
print(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

#transform y into one_hot
one_hot = OneHotEncoder()
y_train = one_hot.fit_transform(y_train)
y_test = one_hot.transform(y_test)

print(x_train[0])

print(y_train[0])

x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)

print(x_train[0])

print(y_train[0])

x_train.shape[1]

y_train.shape

model = Sequential()
model.add(layers.Embedding(max_features, 256,input_length=x_train.shape[1])) 
model.add(layers.LSTM(64))
model.add(layers.Dense(1, activation='sigmoid')) 


model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['acc']) 


history = model.fit(x_train, np.asarray(y_train.tocoo().col),validation_data=(x_test,np.asarray(y_test.tocoo().col)),epochs=20,
                    batch_size=500,
                    validation_split=0.2)
print(model.summary())

