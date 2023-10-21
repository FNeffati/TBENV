import os

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__,  static_folder='../tb_env_react/build/')
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
