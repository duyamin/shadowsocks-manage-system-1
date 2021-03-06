# coding:utf-8
import json
import os

import flask_login
from flask_login import login_required, logout_user, login_user
from flask import Flask, abort, g, jsonify, make_response, request, url_for

from models.database.database import db_session
from models.user import User

app = Flask(__name__)
app.secret_key = 'debudedebude'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


def init_db():
    import models
    from models.database.database import Base, engine
    Base.metadata.create_all(bind=engine)

@login_manager.user_loader
def load_user(id):
    if not id:
        return None
    return User.query.get(int(id))

@app.route('/index')
def _index():
    return 'hello flask'

@app.route('/signup', methods=['POST'])
def _signup():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    db_session.add(user)
    db_session.commit()
    return jsonify({'username': user.username})

@app.route('/login')
def _login():
    user = User.query.get(1)
    login_user(user)
    return "login page"

@app.route('/logout')
@login_required
def _logout():
    logout_user()
    return "login page"

@app.route('/test')
@login_required
def test():
    return "yes , you are allowed"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
