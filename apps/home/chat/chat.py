from apps import db
from datetime import datetime


class ChatMessage(db.Model):
    __tablename__ = 'chat_message'

    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(255))
    bot_response = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)