from crypt import methods

from flask import render_template, flash, redirect, url_for
from health_app import app, db, bcrypt
from health_app.forms import LoginForm, RegistrationForm
from health_app.models import Consumer

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user with the form data
        user = Consumer(Email=form.email.data,
                        password=form.password.data,
                        Name=form.name.data,
                        Surname=form.surname.data,
                        DateOfBirth=form.date_of_birth.data,
                        Gender=form.gender.data)
        # Add the user to the database
        db.session.add(user)
        db.session.commit()
        flash(f'Account created!', 'success')
        return redirect(url_for('home'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            msg = f'{err_msg}'
            flash(f'There was an error: {msg[2:-2]}', 'warning')
    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = Consumer.query.filter_by(Email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.PasswordHash, form.password.data):
            flash(f'Login Successfull!', 'success')
        return redirect(url_for('home'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            msg = f'{err_msg}'
            flash(f'There was an error: {msg[2:-2]}', 'warning')
    return render_template('auth/login.html', form=form)