# coding: utf8

from flask import render_template
from flask_login import login_required

from app import app
from app import helpers
from app.views import LoginView


@app.route('/')
@app.route('/index.html')
@login_required
@helpers.title('Home')
def home(*args, **kwargs):
    posts = [
                {
                    'author': {'username': 'Name'},
                    'body': 'Some message'

                },
                {
                    'author': {'username': 'Русский'},
                    'body': 'Русское сообщение'
                }
            ] * 2
    return render_template('index.html', __title__=kwargs['__title__'], **locals())


@app.route('/login', methods=['GET', 'POST'])
def login():
    return LoginView().login()


@app.route('/logout')
def logout():
    return LoginView.logout()
