from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):

    email = StringField(label='Indirizzo Email:', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password:', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label='Conferma Password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Registrati')
