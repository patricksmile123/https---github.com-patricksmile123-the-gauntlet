from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import random
import json
import requests

app = Flask(__name__)
CORS(app)

# Sample word list
WORD_LIST = ["apple", "berry", "cherry", "dates", "elder"]

# Select a random word from the list
SECRET_WORD = random.choice(WORD_LIST)

@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    if not data or 'guess' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    guess = data['guess']
    
    result = []
    for i in range(len(guess)):
        if guess[i] == SECRET_WORD[i]:
            result.append('correct')
        elif guess[i] in SECRET_WORD:
            result.append('present')
        else:
            result.append('absent')
    
    response = {"result": result}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)