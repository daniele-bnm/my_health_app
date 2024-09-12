from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from health_app import  app, db
from health_app.forms import LoginForm, RegistrationForm, ProfileForm, HealthDietForm, PhysicalActivityForm
from health_app.models import Consumer, PhysicalActivity, Activities, HealthConditions, Diet, DietConsumerChoices, ConsumerHealthConditions


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

    form = HealthDietForm()

        # Populate the diet type choices
    form.diet_type.choices = [diet.DietId for diet in Diet.query.all()]

        # Get the user's health conditions and diet
    user_conditions = ConsumerHealthConditions.query.filter_by(Consumer=current_user.ConsumerId).all()
    selected_diet = DietConsumerChoices.query.filter_by(Consumer=current_user.ConsumerId).first()
    context = {'user_conditions': user_conditions, 'selected_diet': selected_diet}

        # Populate the health condition choices
    form.health_conditions.choices = [hc.HealthConditionId for hc in HealthConditions.query.all()]

    chosen_diet = DietConsumerChoices.query.filter_by(Consumer=current_user.ConsumerId).first()

        # Save selected diet
    if form.validate_on_submit():
        if chosen_diet:
            chosen_diet.Diet = form.diet_type.data
        else:
            new_diet = DietConsumerChoices(Consumer=current_user.ConsumerId, Diet=form.diet_type.data)
            db.session.add(new_diet)

        db.session.commit()

        flash('Your selections have been saved!', 'success')
        return redirect(url_for('health_and_diet_page'))

    if request.method == 'POST' and 'delete_condition' in request.form:
        condition_id = request.form['condition_id']
        condition = ConsumerHealthConditions.query.filter_by(Cosnumer=current_user.ConsumerId, HealthConditions=condition_id).first()
        if condition:
            db.session.delete(condition)
            db.session.commit()
            flash('Health condition deleted successfully!', 'success')
            return redirect(url_for('health_and_diet_page'))

    return render_template('app_dir/health_and_diet.html', form=form, context=context)


@app.route('/phisical_activity', methods=['GET', 'POST'])
@login_required
def physical_activity_page():
    form = PhysicalActivityForm()

    # Get the user's activities
    user_activities = PhysicalActivity.query.filter_by(ConsumerId=current_user.ConsumerId).order_by(
        PhysicalActivity.Date.desc()).all()
    context = {'user_activities': user_activities}

    activities = Activities.query.all()
    activities.insert(0, Activities(ActivityId='', SpecificActivity=''))

    # Populate the choices for the activity_type select field
    form.activity_id.choices = [(activity.ActivityId, activity.SpecificActivity) for activity in
                                activities]

    if form.validate_on_submit():
        new_activity = PhysicalActivity(
            ConsumerId=current_user.ConsumerId,
            ActivityId=form.activity_id.data,
            SpecificActivity=Activities.query.filter_by(ActivityId=form.activity_id.data).first().SpecificActivity,
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