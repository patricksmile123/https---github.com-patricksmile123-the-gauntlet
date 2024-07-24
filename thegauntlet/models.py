from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False, index=True)
    lastname = db.Column(db.String(20), nullable=False, unique=True, index=True)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    db.relationship('Leaderboard', backref='user_id', lazy='dynamic')
    db.relationship('Session', backref='user_id', lazy='dynamic')
    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Leaderboard(db.Model):
    game_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)

class Session(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    SessionKey = db.Column(db.String, primary_key=True, unique=True, nullable=False)


