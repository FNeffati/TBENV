import os
import pymongo
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import Analysis
import json

app = Flask(__name__, static_folder='./build/')
CORS(app)

MONGO_URI = "mongodb+srv://Neffati:y4m4SKKmoIg6riCP@cluster0.h1xa7vw.mongodb.net/?retryWrites=true&w=majority"
connection = pymongo.MongoClient(MONGO_URI)

analysis = Analysis.Analysis()

test_dic = {'message': 'hello world', 'college': 'ncf'}


@app.route('/tryDB', methods=['GET'])
def testdb():
    print("TESTER")
    try:
        db = connection.test_database
        insertions = db.insertions
        """
        db = connection.test_database
        insertion = {
            "author": "NCF",
            "text": "My first insertion"
        }
        insertions = db.insertions
        insertions.insert_one(insertion)
        print("Pinged your deployment. You successfully connected to MongoDB!")
        """
        print(insertions.find_one({"author": "NCF"}))
    except Exception as e:
        print(e, "FAILED")

    return "0"


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
    account_type = None

    try:
        time_frame = request_body[0].split(' ')
        county = request_body[1]
        account_type = request_body[2].lower()
        if county == "All":
            county = None
    except Exception as E:
        print(E, "Something went wrong with extracting time frame and county")

    tweets = analysis.get_filtered_tweets(time_frame, county, account_type)
    # tweets = json.loads(tweets)

    return tweets


@app.route('/get_terms', methods=['POST'])
def get_terms():
    request_body = request.get_json()
    type_of_cloud = request_body[0]
    county = request_body[2]

    if type_of_cloud is None:
        type_of_cloud = "Non-Geo Tags"

    result = analysis.get_key_words_frequency(type_of_cloud, county)
    return result


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
