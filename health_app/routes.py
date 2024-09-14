import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from health_app import  app, db
from health_app.forms import LoginForm, RegistrationForm, ProfileForm, PhysicalActivityForm, HealthConditionsForm, \
    DietForm, JoinFamilyForm, BodyCompositionForm
from health_app.models import Consumer, Family, PhysicalActivity, Activities, HealthConditions, Diet, \
    DietConsumerChoices, ConsumerHealthConditions, BodyComposition
import uuid

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/home')
@login_required
def home_page():
    return render_template('home.html')


# View Family Page - Show the current family code and options to join/create/leave family
# View Family Page - Show the current family code and options to join/create/leave family
@app.route('/family', methods=['GET', 'POST'])
@login_required
def family_page():
    # Initialize the join form
    join_form = JoinFamilyForm()

    # Handle join family form submission
    if join_form.validate_on_submit():
        family_to_join = Family.query.filter_by(FamilyId=join_form.existing_family_code.data).first()

        if family_to_join:
            # Update the current user's family and increment the members count
            current_user.Family = family_to_join.FamilyId
            family_to_join.Members += 1
            db.session.commit()
            flash(f'You have successfully joined the family with code {family_to_join.FamilyId}', 'success')
        else:
            flash('Family code does not exist. Please try again.', 'danger')

        return redirect(url_for('family_page'))

    # Fetch family members if the user is part of a family
    family_members = None
    if current_user.Family:
        family_members = Consumer.query.filter_by(Family=current_user.Family).all()

    # Render the template, passing the join_form to the HTML
    return render_template('app_dir/family.html', join_form=join_form, family_members=family_members)


# Route to create a new family
@app.route('/create_family', methods=['POST'])
@login_required
def create_family():
    # Generate a unique family ID using UUID
    family_id = str(uuid.uuid4())[:8]  # Shorten UUID for simplicity
    new_family = Family(FamilyId=family_id, Members=1)
    db.session.add(new_family)
    db.session.commit()

    # Update current user to the new family
    current_user.Family = new_family.FamilyId
    db.session.commit()

    flash(f'You have created a new family with the code {new_family.FamilyId}', 'success')
    return redirect(url_for('family_page'))


# Route to leave the family
@app.route('/leave_family', methods=['POST'])
@login_required
def leave_family():
    # Get the user's current family
    current_family = Family.query.filter_by(FamilyId=current_user.Family).first()

    if current_family:
        # Reduce the family member count
        current_family.Members -= 1
        # Remove the user from the family
        current_user.Family = None

        # If no members are left, delete the family
        if current_family.Members == 0:
            db.session.delete(current_family)

        db.session.commit()
        flash('You have left the family.', 'warning')
    else:
        flash('Error leaving family. You are not part of any family.', 'danger')

    return redirect(url_for('family_page'))

####################
#   Other routes   #
####################
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

    dform = DietForm()
    hform = HealthConditionsForm()

    # Get the user's health conditions and diet
    user_conditions = ConsumerHealthConditions.query.filter_by(Consumer=current_user.ConsumerId).all()
    selected_diets = DietConsumerChoices.query.filter_by(Consumer=current_user.ConsumerId).all()
    context = {'user_conditions': user_conditions, 'selected_diets': selected_diets}

    # Populate the diet type choices
    diets = Diet.query.all()
    dform.diet_type.choices = [(diet.DietId, diet.Description) for diet in diets]
    for diet in selected_diets:
        dform.diet_type.choices.remove((diet.DietId, diet.Description))

    # Populate the health condition choices
    hcs = HealthConditions.query.all()
    hform.health_conditions.choices = [hc.HealthConditionId for hc in hcs]
    for hc in hcs:
        hform.health_conditions.choices.remove(hc.HealthConditionId)


    # Save selected diet
    if dform.validate_on_submit():
        if False:
            ss=1;
        else:
            new_diet = DietConsumerChoices(Consumer=current_user.ConsumerId, Diet=dform.diet_type.data)
            db.session.add(new_diet)
            db.session.commit()

        flash('Your selections have been saved!', 'success')
        return redirect(url_for('health_and_diet_page'))



    if request.method == 'POST' and 'delete_condition' in request.form:
        condition_id = request.form.get('delete_condition')
        condition = ConsumerHealthConditions.query.filter_by(Consumer=current_user.ConsumerId, HealthConditions=condition_id).first()
        if condition:
            db.session.delete(condition)
            db.session.commit()
            flash('Health condition deleted successfully!', 'success')
            return redirect(url_for('health_and_diet_page'))
        else:
            flash('Health condition not found!', 'danger')
            return redirect(url_for('health_and_diet_page'))

    if dform.errors != {} :
        for err_msg in dform.errors.values():
            msg = f'{err_msg}'
            flash(f'Diet form: {msg[2:-2]}', 'warning')

    if hform.errors != {} :
        for err_msg in hform.errors.values():
            msg = f'{err_msg}'
            flash(f'Health conditions form: {msg[2:-2]}', 'warning')


    return render_template('app_dir/health_and_diet.html', context=context)

@app.route('/phisical_activity', methods=['GET', 'POST'])
@login_required
def physical_activity_page():
    form = PhysicalActivityForm()

    # Get the user's activities
    user_activities = PhysicalActivity.query.filter_by(Consumer=current_user.ConsumerId).order_by(PhysicalActivity.Date.desc()).all()
    context = {'user_activities': user_activities}

    # Populate the activity choices
    activities = Activities.query.all()
    activities.insert(0, Activities(ActivityId='', SpecificActivity=''))
    form.activity_id.choices = [(activity.ActivityId, activity.SpecificActivity) for activity in activities]

    if form.validate_on_submit():
        new_physical_activity = PhysicalActivity(
            Consumer=current_user.ConsumerId,
            Activity=form.activity_id.data,
            SpecificActivity=Activities.query.filter_by(ActivityId=form.activity_id.data).first().SpecificActivity,
            DurationMinutes=form.duration_minutes.data,
            Date=form.date.data
        )

        db.session.add(new_physical_activity)
        db.session.commit()

        flash('Activity added successfully!', 'success')
        return redirect(url_for('physical_activity_page'))


    # Check if the form is for deletion
    if request.method == 'POST' and 'delete_activity_id' in request.form:
        physical_activity_id = request.form.get('delete_activity_id')
        # Find the activity to delete
        activity_to_delete = PhysicalActivity.query.filter_by(
            PhysicalActivityId=physical_activity_id
        ).first()

        # If the activity exists, delete it
        if activity_to_delete:
            db.session.delete(activity_to_delete)
            db.session.commit()
        else:
            flash('An error occurred. Activity not found.', 'danger')

        return redirect(url_for('physical_activity_page'))

    return render_template('app_dir/physical_activity.html', form=form, context=context)

@app.route('/update_body_composition', methods=['GET', 'POST'])
@login_required
def body_composition_page():
    form = BodyCompositionForm()

    # Fetch past data for the current user
    past_data = BodyComposition.query.filter_by(Consumer=current_user.ConsumerId).order_by(BodyComposition.Date.desc()).all()

    # Pre-fill the form's height with the latest height, if available
    last_record = BodyComposition.query.filter_by(Consumer=current_user.ConsumerId).order_by(BodyComposition.Date.desc()).first()
    if last_record and request.method == 'GET':
        form.height.data = last_record.Height

    # Calculate BMI based on the most recent data
    bmi = None
    if last_record:
        weight = last_record.Weight
        height_meters = last_record.Height / 100  # Convert height to meters
        if height_meters > 0:
            bmi = round(weight / (height_meters ** 2), 2)

    # Process form submission
    if form.validate_on_submit():
        new_entry = BodyComposition(
            Consumer=current_user.ConsumerId,
            Weight=form.weight.data,
            Height=form.height.data,
            Date=datetime.datetime.now()
        )
        db.session.add(new_entry)
        db.session.commit()
        flash('Your body composition has been updated.', 'success')
        return redirect(url_for('body_composition_page'))

    return render_template('app_dir/body_composition.html', form=form, past_data=past_data, bmi=bmi)

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