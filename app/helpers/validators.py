# coding: utf8

from flask import flash, redirect

from app.models import User

__all__ = ['is_authenticated', 'is_not_current_user', 'is_user_password_valid', 'is_user_exist', ]


def _get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def is_authenticated(func):
    def wrap(self, *args, **kwargs):
        if self.user.is_authenticated:
            return self.default_page

        return func(self, *args, **kwargs)

    return wrap


def is_not_current_user(func):
    @_is_user_exist
    def wrapper(self, user, *args, **kwargs):
        if user and user == self.user:
            flash(f'You cannot {func.__name__} yourself!')
            return redirect(self.default_page)

        return func(self, user.username, *args, **kwargs)

    return wrapper


def is_user_password_valid(func):
    @_is_user_exist
    def wrapper(self, user, password, *args, **kwargs):
        if not user.check_password(password):
            flash(f'Invalid password for user {user.username}')
            return redirect(self.default_page)

        return func(self, user.username, password, *args, **kwargs)

    return wrapper


def is_user_exist(func):
    @_is_user_exist
    def wrapper(self, user, *args, **kwargs):
        return func(self, user.username, *args, **kwargs)

    return wrapper


def _is_user_exist(func):
    def wrapper(self, username, *args, **kwargs):
        user = _get_user_by_username(username)
        if not user:
            flash(f'User with username: "{username}" not found!')
            return redirect(self.default_page)

        return func(self, user, *args, **kwargs)

    return wrapper
