from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, DateField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from health_app.models import Consumer


class RegistrationForm(FlaskForm):

    def validate_email(self, email_to_check):
        if Consumer.query.filter_by(Email=email_to_check.data).first():
            raise ValidationError('Email address already exists! Try logging in instead.')

    email = StringField(label='Indirizzo Email:', validators=[DataRequired(message='Email is required'), Length(max=45), Email()])
    password = PasswordField(label='Password:', validators=[DataRequired(message='Password is required'), Length(min=6)])
    confirm_password = PasswordField(label='Conferma Password:', validators=[DataRequired(message='Please confirm your password'), EqualTo('password')])
    name = StringField(label='Nome:', validators=[DataRequired(message='Please enter your name'), Length(max=45)])
    surname = StringField(label='Cognome:', validators=[DataRequired(message='Please enter your surname'), Length(max=45)])
    date_of_birth = DateField(label='Data di Nascita:', validators=[DataRequired(message='Please enter your date of birth')])
    gender = SelectField(label='Genere:', choices=[('', 'Seleziona'), ('male', 'Maschio'), ('female', 'Femmina')], validators=[DataRequired(message='Please select your gender')])
    submit = SubmitField(label='Crea Account')

class LoginForm(FlaskForm):

    email = StringField(label='Indirizzo Email:', validators=[DataRequired(message='Email is required'), Length(max=45), Email()])
    password = PasswordField(label='Password:', validators=[DataRequired(message='Password is required')])
    submit = SubmitField(label='Accedi')

class ProfileForm(FlaskForm):

    def validate_email(self, email_to_check):
        if Consumer.query.filter_by(Email=email_to_check.data).first() and email_to_check.data != self.email.data:
            raise ValidationError('This email has been registered already!')

    email = StringField(label='Indirizzo Email', validators=[DataRequired(message='Enter a valid email'), Length(max=45), Email()])
    name = StringField(label='Nome', validators=[DataRequired(message='Enter your name'), Length(max=45)])
    surname = StringField(label='Cognome', validators=[DataRequired(message='Enter your surname'), Length(max=45)])
    date_of_birth = DateField(label='Data di Nascita', validators=[DataRequired(message='Please enter your date of birth')])
    place_of_birth = StringField(label='Luogo di Nascita', validators=[Length(max=45)])
    gender = SelectField(label='Genere', choices=[('','Seleziona'),('male', 'Maschio'), ('female', 'Femmina')], validators=[DataRequired(message='Please select your gender')])
    address = StringField(label='Indirizzo', validators=[Length(max=45)])
    submit = SubmitField(label='Salva')



class AddDietForm(FlaskForm):
    diet_choice = SelectField('Add a new Diet:', validators=[DataRequired()], choices=[])
    submit_diet = SubmitField('Add Diet')

class AddHealthConditionForm(FlaskForm):
    condition_choice = SelectField('Add a new Health Condition:', validators=[DataRequired()], choices=[])
    submit_condition = SubmitField('Add Condition')

class PhysicalActivityForm(FlaskForm):
    activity_id = SelectField('Activity', choices=[],validators=[DataRequired()])
    duration_minutes = IntegerField('Duration (Minutes)', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Add Activity')

class JoinFamilyForm(FlaskForm):
    existing_family_code = StringField('Family Code', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Join Family')


class BodyCompositionForm(FlaskForm):
    weight = DecimalField('Weight (kg)', validators=[DataRequired(message='Weight required'), NumberRange(min=0, max=500, message="Weight must be a positive value")])
    height = DecimalField('Height (cm)', validators=[DataRequired(message='Height required'), NumberRange(min=0, max=300, message="Height must be a positive value")])
    submit = SubmitField('Update Body Composition')


class NewPurchaseForm(FlaskForm):
    receipt_id = StringField('Receipt ID:', validators=[DataRequired(message='Please, enter the receipt ID'), Length(max=20)])
    date = DateField('Date:', validators=[DataRequired(message='Purchase date required')], format='%Y-%m-%d')
    product = SelectField('Product:', choices=[], validators=[DataRequired(message='Please, select a product')])
    quantity = IntegerField('Quantity:', validators=[DataRequired(message='Quantity required'), NumberRange(min=1)])
    price = DecimalField('Price:', places=2, validators=[DataRequired(message='Price required'), NumberRange(min=0)])