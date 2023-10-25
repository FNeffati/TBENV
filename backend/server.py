import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

import pandas as pd

app = Flask(__name__, static_folder='../tb_env_react/build/')
CORS(app)


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask!"})


@app.route('/get_tweets', methods=['GET'])
def get_tweets():
    tweets = None
    file_path = 'RedTide_Pasco_all_SIMPLE_columns.csv'

    selected_columns = ['text', 'created_at.x', 'username', 'profile_image_url', 'location']

    try:
        data = pd.read_csv(file_path, usecols=selected_columns)
        data.rename(columns={'created_at.x': 'time', 'profile_image_url': "image"}, inplace=True)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        data = None

    if data is not None:
        tweets = data.to_json(orient='records')

    return tweets


@app.route('/get_terms', methods=['GET'])
def get_terms():
    terms = None
    file_path = 'geo_tags_RedTide_Pasco.csv'

    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        data = None

    if data is not None:
        terms = data.to_json(orient='records')

    return terms


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
