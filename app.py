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

responses = {}
with open("Dataset/intents-rev2.json") as json_data:
    json_dict = json.load(json_data)
    for intents in json_dict['intents']:
        responses[intents['tag']]=intents['responses']

pre_df = pd.read_pickle("pre_df.pkl")

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
    model = keras.models.load_model('mindmate_model.h5')
    # Create a LabelEncoder object
    encoder = LabelEncoder()
    y_train = encoder.fit_transform(pre_df['tags'])
    output_size = encoder.classes_.shape[0]
    tokenizer = Tokenizer(num_words=2000)
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
