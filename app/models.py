from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)  # Optional, if you want authentication
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    moods = db.relationship('Mood', backref='user', lazy=True)
    chats = db.relationship('ChatHistory', backref='user', lazy=True)
    reminders = db.relationship('Reminder', backref='user', lazy=True)

class Mood(db.Model):
    __tablename__ = 'moods'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood = db.Column(db.String(20), nullable=False)
    note = db.Column(db.String(240), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    MOOD_CHOICES = [
        'Happy', 'Sad', 'Anxious', 'Angry', 'Neutral', 'Stressed', 'Excited', 'Tired', 'Lonely', 'Grateful'
    ]

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'bot'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reminder = db.Column(db.String(240), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

# If you want to add more advanced features like resource bookmarks, add another model:
class ResourceBookmark(db.Model):
    __tablename__ = 'resource_bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resource_title = db.Column(db.String(120), nullable=False)
    resource_url = db.Column(db.String(240), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
