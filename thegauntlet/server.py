from flask import Flask, request, jsonify, Response, session
import random
import uuid
from thegauntlet.models import User, Game, WordleGuess
from thegauntlet import app
from flask_cors import CORS, cross_origin
from thegauntlet.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from thegauntlet.db import db
from flask_wtf.csrf import generate_csrf
import jwt
from datetime import datetime
import traceback

CORS(app)
# Sample word list
WORD_LIST = open("wordle_words.txt").read().splitlines()

@app.route('/createGame', methods=['GET'])
def createGame():
    authoHeader = request.headers.get('authorization')
    token = authoHeader.split(" ")[1]
    try:
        decodedJwt = jwt.decode(token, "s{$822Qcg!d*", algorithms=["HS256"])
        user = User.query.filter_by(username=decodedJwt['username']).first()
        currentGame = Game.query.filter_by(user_id=user.user_id).filter_by(outcome=None).first()
        if currentGame != None:
            newGame = Game(
                user_id=user.user_id,
                start_time=datetime.now(),
                answer=random.choice(WORD_LIST)
            )
            db.session.add(newGame)
            db.session.commit()
            print(user.username)
            return jsonify(newGame.game_id)
        else:
            currentGuesses = WordleGuess.query.filter_by(game_id = currentGame.game_id).order_by(WordleGuess.guess_time.asc()).all()
            currentGuesses = [guess.guess for guess in currentGuesses]

    except:
        print(traceback.format_exc())
        return jsonify({"error": "Invalid token"}), 400


@app.route('/guess', methods=['POST'])
@cross_origin()
def guess():
    authoHeader = request.headers.get('authorization')
    token = authoHeader.split(" ")[1]
    try:
        decodedJwt = jwt.decode(token, "s{$822Qcg!d*", algorithms=["HS256"])
        user = User.query.filter_by(username=decodedJwt['username']).first()
        currentGame = Game.query.filter_by(user_id=user.user_id).order_by(Game.game_id.desc()).first()
        data = request.get_json()
        if not data or 'guess' not in data:
            return jsonify({"error": "Invalid input"}), 400
        guess = data['guess'].lower()
        dbGuess = WordleGuess(
            game_id=currentGame.game_id,
            guess=guess,
            guess_time=datetime.now()
        )
        db.session.add(dbGuess)

        if guess == currentGame.answer:
            currentGame.end_time = datetime.now()
            currentGame.outcome = "win"
        guessCount = WordleGuess.query.filter_by(game_id=currentGame.game_id).count()
        if guessCount >= len(currentGame.answer):
            currentGame.end_time = datetime.now()
            currentGame.outcome = "loss"
        db.session.commit()
        result = []
        for i in range(len(guess)):
            if guess[i] == currentGame.answer[i]:
                result.append('correct')
            elif guess[i] in currentGame.answer:
                result.append('present')
            else:
                result.append('absent')      
        response = {"result": result, "guessCount": WordleGuess.query.filter_by(game_id=currentGame.game_id).count()}
        return jsonify(response)
    except:
        return jsonify({"error": "Invalid token"}), 400


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
        encodedJwt = jwt.encode({"username": user.username}, "s{$822Qcg!d*", algorithm="HS256")
        return jsonify({"username": user.username, "token": encodedJwt}), 200