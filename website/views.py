from flask import Blueprint, render_template, redirect, request, session
from flask_login import login_required, current_user
from .extensions import socketio
from .models import History


views = Blueprint('views', __name__)



@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    return render_template('home.html', user=current_user)



# @views.route('/chatroom', methods=['POST', 'GET'])
# def chatroom():
#     return render_template('chatroom.html', user=current_user)


