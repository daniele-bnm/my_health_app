from random import choice

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from health_app.models import Consumer


class RegistrationForm(FlaskForm):

    def validate_email(self, email_to_check):
        user = Consumer.query.filter_by(Email=email_to_check.data).first()
        if user:
            raise ValidationError('Email address already exists! Try logging in instead.')

    email = StringField(label='Indirizzo Email:', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password:', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label='Conferma Password:', validators=[DataRequired(), EqualTo('password')])
    name = StringField(label='Nome:', validators=[DataRequired()])
    surname = StringField(label='Cognome:', validators=[DataRequired()])
    date_of_birth = DateField(label='Data di Nascita:', validators=[DataRequired()])
    gender = SelectField(label='Genere:', choices=[('', 'Seleziona'), ('male', 'Maschio'), ('female', 'Femmina')], validators=[DataRequired()])
    submit = SubmitField(label='Registrati')

class LoginForm(FlaskForm):

    email = StringField(label='Indirizzo Email:', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Accedi')