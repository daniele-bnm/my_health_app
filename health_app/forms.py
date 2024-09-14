from random import choice

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, DateField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from health_app.models import Consumer


class RegistrationForm(FlaskForm):

    def validate_email(self, email_to_check):
        if Consumer.query.filter_by(Email=email_to_check.data).first():
            raise ValidationError('Email address already exists! Try logging in instead.')

    email = StringField(label='Indirizzo Email:', validators=[DataRequired(message='Email is required'), Email()])
    password = PasswordField(label='Password:', validators=[DataRequired(message='Password is required'), Length(min=6)])
    confirm_password = PasswordField(label='Conferma Password:', validators=[DataRequired(message='Please confirm your password'), EqualTo('password')])
    name = StringField(label='Nome:', validators=[DataRequired(message='Please enter your name')])
    surname = StringField(label='Cognome:', validators=[DataRequired(message='Please enter your surname')])
    date_of_birth = DateField(label='Data di Nascita:', validators=[DataRequired(message='Please enter your date of birth')])
    gender = SelectField(label='Genere:', choices=[('', 'Seleziona'), ('male', 'Maschio'), ('female', 'Femmina')], validators=[DataRequired(message='Please select your gender')])
    submit = SubmitField(label='Crea Account')

class LoginForm(FlaskForm):

    email = StringField(label='Indirizzo Email:', validators=[DataRequired(message='Email is required'), Email()])
    password = PasswordField(label='Password:', validators=[DataRequired(message='Password is required')])
    submit = SubmitField(label='Accedi')

class ProfileForm(FlaskForm):
    email = StringField(label='Indirizzo Email', validators=[DataRequired(message='Enter a valid email'), Email()])
    name = StringField(label='Nome', validators=[DataRequired(message='Enter your name')])
    surname = StringField(label='Cognome', validators=[DataRequired(message='Enter your surname')])
    date_of_birth = DateField(label='Data di Nascita', validators=[DataRequired(message='Please enter your date of birth')])
    place_of_birth = StringField(label='Luogo di Nascita')
    gender = SelectField(label='Genere', choices=[('','Seleziona'),('male', 'Maschio'), ('female', 'Femmina')], validators=[DataRequired(message='Please select your gender')])
    address = StringField(label='Indirizzo')
    submit = SubmitField(label='Salva')

    def validate_email(self, email_to_check):
        if Consumer.query.filter_by(Email=email_to_check.data).first() and email_to_check.data != self.email.data:
            raise ValidationError('This email has been registered already!')

class DietForm(FlaskForm):
    diet_type = SelectField('Diet Type', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')

class HealthConditionsForm(FlaskForm):
    health_conditions = SelectField('Health Conditions', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')

class PhysicalActivityForm(FlaskForm):
    activity_id = SelectField('Activity', choices=[],validators=[DataRequired()])
    duration_minutes = IntegerField('Duration (Minutes)', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Add Activity')

class JoinFamilyForm(FlaskForm):
    existing_family_code = StringField('Family Code', validators=[DataRequired(), Length(min=4, max=8)])
    submit = SubmitField('Join Family')


class BodyCompositionForm(FlaskForm):
    weight = DecimalField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0, message="Weight must be a positive value")])
    height = DecimalField('Height (cm)', validators=[DataRequired(), NumberRange(min=0, message="Height must be a positive value")])
    submit = SubmitField('Update Body Composition')
