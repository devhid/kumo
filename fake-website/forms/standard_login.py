"""
Simple form for logging in
"""
from wtforms import Form, StringField, PasswordField

class StandardLogin(Form):
    email = StringField('Email')
    password = PasswordField('Password')