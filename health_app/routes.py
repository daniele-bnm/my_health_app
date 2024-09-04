from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from health_app import  app, db
from health_app.forms import LoginForm, RegistrationForm, ProfileForm
from health_app.models import Consumer

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/home')
@login_required
def home_page():
    return render_template('home.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.Email = form.email.data
        current_user.Name = form.name.data
        current_user.Surname = form.surname.data
        current_user.DateOfBirth = form.date_of_birth.data
        current_user.PlaceOfBirth = form.place_of_birth.data
        current_user.Gender = form.gender.data
        current_user.Address = form.address.data

        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('home_page'))
    return render_template('app_dir/profile.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
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
        login_user(user)
        flash(f'Account created!', 'success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            msg = f'{err_msg}'
            flash(f'There was an error: {msg[2:-2]}', 'warning')
    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        user = Consumer.query.filter_by(Email=form.email.data).first()
        if user and user.check_password_hash(form.password.data):
                login_user(user)
                return redirect(url_for('home_page'))
        else:
            flash('Invalid email or password', 'warning')
    if form.errors != {}:
        for err_msg in form.errors.values():
            msg = f'{err_msg}'
            flash(f'There was an error: {msg[2:-2]}', 'warning')
    return render_template('auth/login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("landing_page"))