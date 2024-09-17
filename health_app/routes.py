from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func
from health_app import  app, db
from health_app.forms import LoginForm, RegistrationForm, ProfileForm, PhysicalActivityForm, HealthConditionsForm, \
    DietForm, JoinFamilyForm, BodyCompositionForm, AddPurchaseForm
from health_app.models import Consumer, Family, PhysicalActivity, Activities, HealthConditions, Diet, \
    DietConsumerChoices, ConsumerHealthConditions, BodyComposition, Product, Purchases
import uuid, datetime

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/home')
@login_required
def home_page():
    return render_template('home.html')

####################
#   Family routes  #
####################
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

########################
#   Purchases routes   #
########################

@app.route('/purchases', methods=['GET', 'POST'])
@login_required
def purchases_page():

    form = AddPurchaseForm()

    products = Product.query.all()
    form.product.choices = [(p.ProductId, p.Description) for p in products]

    # Handle form submission to add a new purchase
    if form.validate_on_submit():
        if not current_user.Family:
            flash('Error adding purchase. You are not part of a family.', 'danger')
            return redirect(url_for('purchases_page'))
        else:
            new_purchase = Purchases(
                PurchaseID=form.purchase_id.data,
                Date=form.date.data,
                Quantity=form.quantity.data,
                Price=form.price.data * form.quantity.data,
                Product=form.product.data,
                Family=current_user.Family
            )
            db.session.add(new_purchase)
            db.session.commit()
            flash('Purchase added successfully!', 'success')
            return redirect(url_for('purchases_page'))

    # Query past purchases for the family
    family_id = current_user.Family
    if family_id is None:
        past_purchases=[]
    else:
        past_purchases = db.session.query(
            Purchases.PurchaseID,
            Purchases.Date,
            func.sum(Purchases.Price).label('TotalPrice')
        ).filter_by(Family=family_id).order_by(Purchases.Date.desc()).group_by(Purchases.PurchaseID, Purchases.Date).all()

    return render_template('app_dir/purchases.html', form=form, past_purchases=past_purchases)

@app.route('/purchase/<purchase_id>', methods=['GET'])
@login_required
def purchase_details(purchase_id):
    purchase_items = Purchases.query.filter_by(PurchaseID=purchase_id).all()
    return jsonify([
        {
            "product_description": Product.query.get(item.Product).Description,
            "quantity": item.Quantity,
            "price": float(item.Price)
        } for item in purchase_items
    ])

@app.route('/delete_purchase/', methods=['POST'])
@login_required
def delete_purchase():
    if request.method == 'POST' and 'delete_purchaseid' in request.form:
        purchase_id = request.form.get('delete_purchaseid')
        purchases = Purchases.query.filter_by(PurchaseID=purchase_id).all()
        for item in purchases:
            db.session.delete(item)
            db.session.commit()
        else:
            flash('An error occurred. Couldn\'t delete.', 'danger')

    return redirect(url_for('purchases_page'))

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
            ss=1
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

@app.route('/body_composition', methods=['GET', 'POST'])
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

@app.route('/delete_body_composition', methods=['POST'])
@login_required
def delete_body_composition():

    if request.method == 'POST' and 'delete_record' in request.form:
        body_comp_date = request.form.get('delete_record')
        record_to_delete = BodyComposition.query.filter_by(Consumer=current_user.ConsumerId, Date=body_comp_date).first()
        if record_to_delete:
            db.session.delete(record_to_delete)
            db.session.commit()
        else:
            flash('An error occurred. Couldn\'t delete.', 'danger')

    return redirect(url_for('body_composition_page'))

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