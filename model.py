import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import sent_tokenize
from nltk import word_tokenize
import numpy as np
import tensorflow as tf
import json
import pickle
import random
from googletrans import Translator

nltk.download('punkt')
nltk.download('wordnet')

with open('intents3.json') as intents:
  data = json.load(intents)

lemma = WordNetLemmatizer()

stemmer = LancasterStemmer()
# getting informations from intents.json
words = []
labels = []
x_docs = []
y_docs = []

for intent in data['intents']:
    # Get the 'patterns' array for each intent
    patterns = intent.get('pattern', [])

    # Iterate over patterns for each intent
    for pattern in patterns:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        x_docs.append(wrds)
        y_docs.append(intent['tag'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
words = sorted(list(set(words)))
labels = sorted(labels)

training = []
output = []
out_empty = [0 for _ in range(len(labels))]


# One hot encoding, Converting the words to numerals
for x, doc in enumerate(x_docs):
    bag = []
    wrds = [stemmer.stem(w) for w in doc]
    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)


    output_row = out_empty[:]
    output_row[labels.index(y_docs[x])] = 1

    training.append(bag)
    output.append(output_row)


training = np.array(training)
output = np.array(output)
#print(training)

training = np.array(training)
output = np.array(output)

# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.layers import Dropout

# model = Sequential([
#     Dense(32, input_shape=(len(training[0]),), activation='relu'),
#     Dropout(0.2),
#     Dense(128, activation='relu'),
#     Dropout(0.2),
#     Dense(128, activation='relu'),
#     Dropout(0.2),
#     Dense(len(output[0]), activation='softmax')
# ])
# # Compile the model
# from tensorflow.keras.optimizers import Adam

# model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])

# # Train the model
# model.fit(training, output, epochs=500, batch_size=8, verbose=1)

# # Save the model
# model.save('model_keras.h5')


def translate_hindi_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, src='hi', dest='en')
    return translated_text.text

def translate_english_to_hindi(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='hi')
    return translated_text.text


def translate_text(text, source_language=None):
    translator = Translator()
    # # Detect the source language if not provided
    if source_language is None:
        detected_lang = translator.detect(text)
        source_language = detected_lang.lang

    # Translate the text
    translated_text = translator.translate(text, src=source_language, dest="en")
    list=[source_language,translated_text.text]
    return list

