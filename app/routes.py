# coding: utf8

from flask import render_template
from flask_login import login_required

from app import app
from app import helpers
from app.views import LoginView, RegisterView, UserView, EditProfileView, FollowView


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    return RegisterView().register()


@app.route('/user/<username>')
@login_required
def user(username):
    return UserView(username).user_home_page()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return EditProfileView().edit()


@app.route('/follow/<username>')
@login_required
def follow(username):
    return FollowView().follow(username)


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    return FollowView().unfollow(username)
