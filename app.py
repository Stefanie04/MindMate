from flask import Flask, render_template, request, jsonify
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import numpy as np
import re
import json
import random
import pandas as pd
import os
import pickle

tags = []
patterns = []
responses = {}

my_dir = os.path.dirname(__file__)
json_file_path = os.path.join(my_dir, 'Dataset/intents-rev2.json')
with open(json_file_path) as json_data:
    json_dict = json.load(json_data)
    for intents in json_dict['intents']:
        responses[intents['tag']]=intents['responses']
        for lines in intents['patterns']:
            patterns.append(lines)
            tags.append(intents['tag'])

# loading
my_dir = os.path.dirname(__file__)
tokenizer = None
tokenizer_path = os.path.join(my_dir, 'tokenizer.pkl')
with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

encoder_path = os.path.join(my_dir, 'encoder.pkl')
pkl_file = open(encoder_path, 'rb')
encoder = pickle.load(pkl_file) 
pkl_file.close()

model_path = os.path.join(my_dir, 'mindmate_model.h5')
model = keras.models.load_model(model_path)

input_size=21
output_size=166

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mindMateS3cr3t!'

input_size = 21

@app.route('/', methods=("GET", "POST"))
def index():
    return render_template('index.html')


@app.route('/predict', methods=["POST"])
def predict():
    conversation = []
    request_data = request.get_json()
    user_input = request_data['data']
    toReturn = {"output": "Thank you!"}
    user_input = user_input.lower()
    user_input = re.sub(r'[^\w\s]', '', user_input)
    conversation.append(user_input)

    # tokenizer / padding
    user_input = tokenizer.texts_to_sequences(conversation)
    user_input = np.array(user_input).reshape(-1)
    user_input = pad_sequences([user_input], input_size)

    # output
    output = model.predict(user_input)
    output = output.argmax()

    # prediction
    response = encoder.inverse_transform([output])[0]
    print('response=' + response)
    if response in responses:
        print('MindMate: ', random.choice(responses[response]))
        toReturn = {"output": random.choice(responses[response])}
    else:
        print('Sorry, I do not understand. Can you please rephrase? response='+ response)
        toReturn = {"output": "Sorry, I do not understand. Can you please rephrase?"}
    #if response == 'goodbye':
        #print('goodbye')

    return jsonify(toReturn)
