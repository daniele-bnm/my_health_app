from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from health_app import  app, db
from health_app.forms import LoginForm, RegistrationForm, ProfileForm, HealthDietForm, PhysicalActivityForm
from health_app.models import Consumer, PhysicalActivity, Activities


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
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.Name = form.name.data
        current_user.Surname = form.surname.data
        current_user.Email = form.email.data
        current_user.DateOfBirth = form.date_of_birth.data
        current_user.PlaceOfBirth = form.place_of_birth.data
        current_user.Gender = form.gender.data
        current_user.Address = form.address.data
        db.session.commit()
        flash('Consumer info updated successfully', 'success')
        return redirect(url_for('profile_page'))
    elif request.method == 'GET':
        form.name.data = current_user.Name
        form.surname.data = current_user.Surname
        form.email.data = current_user.Email
        form.date_of_birth.data = current_user.DateOfBirth
        form.place_of_birth.data = current_user.PlaceOfBirth
        form.gender.data = current_user.Gender
        form.address.data = current_user.Address
    if form.errors != {}:
        for err_msg in form.errors.values():
            msg = f'{err_msg}'
            flash(f'{msg[2:-2]}', 'danger')

    return render_template('app_dir/profile.html', form=form)

@app.route('/health_and_diet', methods=['GET', 'POST'])
@login_required
def health_and_diet_page():
    form = HealthDietForm(obj=current_user)
    #if form.validate_on_submit():

    return render_template('app_dir/health_and_diet.html')


@app.route('/phisical_activity', methods=['GET', 'POST'])
@login_required
def physical_activity_page():
    form = PhysicalActivityForm()

    user_activities = PhysicalActivity.query.filter_by(ConsumerId=current_user.ConsumerId).order_by(
        PhysicalActivity.Date.desc()).all()
    activities = Activities.query.all()
    context = {'user_activities': user_activities, 'activities': activities}

    if form.validate_on_submit():
        new_activity = PhysicalActivity(
            ConsumerId=current_user.ConsumerId,
            ActivityId=form.activity_id.data,
            ActivityType=form.activity_type.data,
            DurationMinutes=form.duration_minutes.data,
            Date=form.date.data
        )

        db.session.add(new_activity)
        db.session.commit()

        flash('Activity added successfully!', 'success')
        return redirect(url_for('physical_activity_page'))


    # Check if the form is for deletion
    if request.method == 'POST' and 'delete_activity_id' in request.form:
        activity_id = request.form.get('delete_activity_id')
        consumer_id = request.form.get('delete_consumer_id')
        date = request.form.get('delete_date')

        # Find the activity to delete
        activity_to_delete = PhysicalActivity.query.filter_by(
            ConsumerId=consumer_id,
            ActivityId=activity_id,
            Date=date
        ).first()

        # If the activity exists, delete it
        if activity_to_delete:
            db.session.delete(activity_to_delete)
            db.session.commit()
        else:
            flash('An error occurred. Activity not found.', 'danger')

        return redirect(url_for('physical_activity_page'))

    return render_template('app_dir/physical_activity.html', form=form, context=context)

            ##########################
            # Login and Registration #
            ##########################

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
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
            flash(f'{msg[2:-2]}', 'warning')
    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
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
            flash(f'{msg[2:-2]}', 'warning')
    return render_template('auth/login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("landing_page"))