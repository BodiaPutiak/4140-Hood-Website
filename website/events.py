from .extensions import socketio
from flask import Blueprint, request
from flask_socketio import emit, send
from flask_login import current_user
import time
from .extensions import db
from .models import History
events = Blueprint('events', __name__)

users = {}

@socketio.on("connect")
def handle_connect():
    print('Client connected')

@socketio.on("user_join")
def handle_user_join():
    username = current_user.first_name
    print(f'User {username} joined')
    users[username] = request.sid
    emit('user_join_message', {'message': f'User {username} joined'}, broadcast=True)
    
    chat_history = History.query.order_by(History.date).all()
    chat_history_dict = [{'sender': message.sender, 'content': message.message, 'date': message.date.strftime('%b-%d %I:%M%p')} for message in chat_history]
    emit('chat_history', chat_history_dict)

@socketio.on('incoming-msg')
def on_message(data):
    msg = data['msg']
    username = data['username']
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    messages = History(message=msg, sender=current_user.first_name)
    db.session.add(messages)
    db.session.commit()
    print(f'New message: {msg}')
    send({'username': username, 'msg': msg, 'time_stamp': time_stamp}, broadcast=True)

