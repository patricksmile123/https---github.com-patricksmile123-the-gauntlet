from flask import Flask, request, jsonify, Response
import random
import uuid
import english_words
from flask import Flask
from thegauntlet.models import User, Leaderboard, Session
from thegauntlet import app
from flask_cors import CORS, cross_origin
from thegauntlet.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash
from thegauntlet.db import db


CORS(app)
# Sample word list
WORD_LIST = list(english_words.get_english_words_set(['gcide'], lower=True))
guessCount = 0
game = ""
# Select a random word from the list
SECRET_WORD = ""

@app.route('/createGame', methods=['GET'])
def createGame():
    global game
    game = uuid.uuid4()
    global guessCount
    guessCount = 0
    global SECRET_WORD
    SECRET_WORD = random.choice(WORD_LIST)
    WORD_LIST.remove(SECRET_WORD)
    while len(SECRET_WORD) != 5:
        SECRET_WORD = random.choice(WORD_LIST)
        WORD_LIST.remove(SECRET_WORD)
        print(SECRET_WORD)
    i = {"game": game}
    return jsonify(i)

@app.route('/guess', methods=['POST'])
@cross_origin()
def guess():
    global guessCount
    guessCount += 1
    data = request.get_json()
    if not data or 'guess' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    guess = data['guess'].lower()
    result = []
    for i in range(len(guess)):
        if guess[i] == SECRET_WORD[i]:
            result.append('correct')
        elif guess[i] in SECRET_WORD:
            result.append('present')
        else:
            result.append('absent')
    
    gameOver = {"result": result, "guessCount": guessCount}

    if guessCount == 5:
        return jsonify(gameOver)
    response = {"result": result, "guessCount": guessCount}
    return jsonify(response)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json
    if not data or 'username' and 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, password_hash=generate_password_hash(form.password.data, salt_length=32))
        db.session.add(new_user)
        db.session.commit()