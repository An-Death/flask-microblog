# coding: utf8

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    post = TextAreaField('Whats up, bro?', validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Post')
