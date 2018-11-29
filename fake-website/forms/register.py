"""
Register form for website.
"""
from wtforms import Form, StringField, IntegerField, PasswordField, BooleanField, DateField, RadioField, SelectField

class Register(Form):

    subscription_types = [('Free', 'Free'), ('Plus', 'Plus'), ('Premium', 'Premium')]

    name = StringField('Name')
    gender = RadioField('Gender', choices = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    email = StringField('Email')
    password = PasswordField('Password')
    city = StringField('City')
    country = StringField('Country')
    subscription = SelectField('Subscription', choices = subscription_types)