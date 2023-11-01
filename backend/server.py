import os
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import Analysis
import json

app = Flask(__name__, static_folder='../tb_env_react/build/')
CORS(app)

analysis = Analysis.Analysis()


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


@app.route('/get_tweets', methods=['POST'])
def get_tweets():
    request_body = request.get_json()

    time_frame = None
    county = None

    try:
        time_frame = request_body[0]
        county = request_body[1]
    except Exception as E:
        print(E, "Something went wrong with extracting time frame and county")

    filtered_tweets = analysis.get_filtered_tweets(time_frame, county)
    tweets = filtered_tweets.to_json(orient='records')

    return tweets


@app.route('/get_terms', methods=['POST'])
def get_terms():
    request_body = request.get_json()
    type_of_cloud = request_body[0]
    if type_of_cloud is None:
        type_of_cloud = "Non-Geo Tags"

    terms = []

    try:
        data = analysis.get_key_words_frequency(type_of_cloud)

    except Exception as E:
        print(E, "COULDN'T GET TERMS FOR SOME REASON")
        data = None

    if data is not None:
        terms = [{'text': key, 'value': data[key]} for key in data]
    return terms


@app.route('/get_counties', methods=['GET'])
def get_counties():
    file_path = 'fl-counties.json'

    try:
        with open(file_path, 'r') as file:
            counties = json.load(file)
            return jsonify(counties)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        data = None

    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
