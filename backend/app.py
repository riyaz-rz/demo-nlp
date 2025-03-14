from flask import Flask, request, jsonify
from flask_cors import CORS



print("hello world")


app = Flask(__name__)
CORS(app)
@app.route('/search', methods=['GET'])
def query():
    return "It is from the API"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)