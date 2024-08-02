from flask import Flask, request, jsonify, Response, session
import random
import uuid
from thegauntlet.models import User, Leaderboard
from thegauntlet import app
from flask_cors import CORS, cross_origin
from thegauntlet.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from thegauntlet.db import db
from flask_wtf.csrf import generate_csrf
from pyjwt import jwt, JWTError


CORS(app)
# Sample word list
WORD_LIST = open("wordle_words.txt").read().splitlines()
guessCount = 0
game = ""
# Select a random word from the list
SECRET_WORD = ""

@app.route('/createGame', methods=['GET'])
def createGame():
    global game
    game = uuid.uuid4()
    global WORD_LIST
    global guessCount
    guessCount = 0
    global SECRET_WORD
    SECRET_WORD = random.choice(WORD_LIST)
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
    print("SIGNUP FUNCTION CALLED")
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    form = RegistrationForm(data=data)
    #print("signup", session['csrf_token'])
    if form.validate_on_submit():
        print("Form is valid")
        new_user = User(
            username=form.username.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            password_hash=generate_password_hash(form.password.data, salt_length=32)
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    else:
        errors = form.errors
        return jsonify({'errors': errors}), 400


@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    session['csrf_token'] = token
    print("get_csrf_token", session['csrf_token'])
    return jsonify({'csrf_token': session['csrf_token']})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400
    form = LoginForm(data=data)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user == None:
            return jsonify({"error": "User not found"}), 404
        if check_password_hash(user.password_hash, form.password.data) == False or form.password.data == None:
            return jsonify({"error": "Invalid Username or Password"}), 400
        encoded_jwt = jwt.encode({"username": user.username}, "s{$822Qcg!d*", algorithm="HS256")
        return jsonify({"username": user.username, "token": encoded_jwt}), 200