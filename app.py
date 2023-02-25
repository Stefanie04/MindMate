from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mindMateS3cr3t!'


@app.route('/', methods=("GET", "POST"))
def index():
    return render_template('index.html')


@app.route('/predict', methods=["POST"])
def predict():
    request_data = request.get_json()
    data = request_data['data']
    toReturn = {"output": "Predicted Output= " + data}

    return jsonify(toReturn)
