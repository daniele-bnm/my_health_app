from flask import render_template, flash, redirect, url_for
from health_app import app, db
from health_app.forms import RegistrationForm
from health_app.models import Consumer


@app.route('/')
def landing_page():
    return render_template('landing_page.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user with the form data
        user = Consumer(email=form.email.data, password_hash=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('home'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error: {err_msg}', 'warning')
    return render_template('register.html', form=form)

@app.route('/home')
def home():
    return render_template('home.html')