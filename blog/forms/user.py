from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField


class UserBaseForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    username = StringField(
        'Username',
        [validators.DataRequired()],
    )
    email = StringField(
        'Email address',
        [
            validators.DataRequired(),
            validators.Email(),
            validators.Length(min=6, max=200),
        ],
        filters=[lambda data: data and data.lower()]
    )


class RegistrationForm(UserBaseForm):
    password = PasswordField(
        'Password',
        [
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords must match'),
        ],
    )
    confirm = PasswordField('Repeat password')
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        [validators.DataRequired()],
    )
    password = PasswordField(
        'Password',
        [validators.DataRequired()]
    )
    submit = SubmitField('Login')
