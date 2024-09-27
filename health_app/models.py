from health_app import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Consumer.query.get(int(user_id))

class Consumer(db.Model, UserMixin):
    __tablename__ = 'Consumer'
    ConsumerId = db.Column(db.Integer, autoincrement=True, unique=True, index=True, primary_key=True, nullable=False)
    Email = db.Column(db.String(45), nullable=False, unique=True)
    PasswordHash = db.Column(db.String(255), nullable=False)
    Name = db.Column(db.String(45), nullable=False)
    Surname = db.Column(db.String(45), nullable=True)
    DateOfBirth = db.Column(db.Date, nullable=False)
    PlaceOfBirth = db.Column(db.String(45), nullable=True)
    Gender = db.Column(db.Enum('male', 'female', name='enum_gender'), nullable=False)
    Family = db.Column(db.String(10), db.ForeignKey('Family.FamilyId'), nullable=True)
    Role = db.Column(db.String(45), nullable=True)
    Address = db.Column(db.String(45), nullable=True)
    BodyCompositions = db.relationship('BodyComposition', lazy=True)

    @property
    def password(self):
        return self.PasswordHash

    @password.setter
    def password(self, plain_text_password):
        self.PasswordHash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_hash(self, attempted_password):
        return bcrypt.check_password_hash(self.PasswordHash, attempted_password)

    def get_id(self):
        return self.ConsumerId


class BodyComposition(db.Model):
    __tablename__ = 'BodyComposition'
    Consumer = db.Column(db.String(45), db.ForeignKey('Consumer.ConsumerId', ondelete='CASCADE'), primary_key=True, nullable=False)
    Date = db.Column(db.DateTime, primary_key=True, nullable=False)
    Weight = db.Column(db.Numeric(5, 2), nullable=True)
    Height = db.Column(db.Numeric(5, 1), nullable=True)

class Family(db.Model):
    __tablename__ = 'Family'
    FamilyId = db.Column(db.String(10), primary_key=True, nullable=False)
    Description = db.Column(db.String(255), nullable=True)
    Members = db.Column(db.Integer, nullable=True)

class DietConsumerChoices(db.Model):
    __tablename__ = 'DietConsumerChoices'
    Consumer = db.Column(db.Integer, db.ForeignKey('Consumer.ConsumerId'), primary_key=True, nullable=False)
    Diet = db.Column(db.Integer, db.ForeignKey('Diet.DietId'), primary_key=True, nullable=False)

class Diet(db.Model):
    __tablename__ = 'Diet'
    DietId = db.Column(db.String(50), primary_key=True, nullable=False)
    Description = db.Column(db.String(45), nullable=True)
    RestrictionLevel = db.Column(db.Integer, nullable=True)

class PhysicalActivity(db.Model):
    __tablename__ = 'PhysicalActivity'
    PhysicalActivityId = db.Column(db.Integer, primary_key=True, nullable=False)
    Activity = db.Column(db.Integer, db.ForeignKey('Activities.ActivityId'), nullable=False)
    Consumer = db.Column(db.Integer, db.ForeignKey('Consumer.ConsumerId'), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    SpecificActivity = db.Column(db.Text, nullable=False)
    DurationMinutes = db.Column(db.Integer, nullable=False)

class Activities(db.Model):
    __tablename__ = 'Activities'
    ActivityId = db.Column(db.Integer, primary_key=True, nullable=False)
    ActivityType = db.Column(db.String(50), nullable=True)
    MET = db.Column(db.Numeric(5, 2), nullable=True)
    SpecificActivity = db.Column(db.Text, nullable=True)

class ConsumerHealthConditions(db.Model):
    __tablename__ = 'ConsumerHealthConditions'
    Consumer = db.Column(db.Integer, db.ForeignKey('Consumer.ConsumerId', ondelete='CASCADE'), primary_key=True, nullable=False)
    HealthConditions = db.Column(db.String(100), db.ForeignKey('HealthConditions.HealthConditionId', ondelete='CASCADE'), primary_key=True, nullable=False)

class HealthConditions(db.Model):
    __tablename__ = 'HealthConditions'
    HealthConditionId = db.Column(db.String(100), primary_key=True, nullable=False)
    Description = db.Column(db.Text)

class NutrientHealthConditions(db.Model):
    __tablename__ = 'NutrientHealthConditions'
    HealthCondition = db.Column(db.String(100), db.ForeignKey('HealthConditions.HealthConditionId'), primary_key=True, nullable=False)
    Nutrient = db.Column(db.String(100), db.ForeignKey('NutritionalInformation.NutrientId', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    MinQuantity = db.Column(db.Integer, default=None)
    MaxQuantity = db.Column(db.Integer, default=None)
    # db.Boolean for PercentKCal and UoMperKg columns as they are defined as tinyint(1) MySQL
    PercentKCal = db.Column(db.Boolean, default=None)
    UoMperKg = db.Column(db.Boolean, default=None)

class NutritionalInformation(db.Model):
    __tablename__ = 'NutritionalInformation'
    NutrientId = db.Column(db.String(100), primary_key=True, nullable=False)
    NutrientIT = db.Column(db.String(100), nullable=False)
    UnitOfMeasure = db.Column(db.String(255), default=None)

class Allergens(db.Model):
    __tablename__ = 'Allergens'
    AllergenId = db.Column(db.String(25), primary_key=True, nullable=False)
    AllergenName = db.Column(db.String(45), default=None)

class Product(db.Model):
    __tablename__ = 'Product'
    ProductId = db.Column(db.String(20), primary_key=True, nullable=False)
    Description = db.Column(db.String(200), default=None)
    ProductCategory = db.Column(db.String(100), db.ForeignKey('ProductCategory.ProductCategoryId', ondelete='CASCADE', onupdate='CASCADE'), default=None)

class ProductAllergens(db.Model):
    __tablename__ = 'ProductAllergens'
    Product = db.Column(db.String(20), db.ForeignKey('Product.ProductId', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    Allergens = db.Column(db.String(25), db.ForeignKey('Allergens.AllergenId', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)

class ProductCategory(db.Model):
    __tablename__ = 'ProductCategory'
    ProductCategoryId = db.Column(db.String(100), primary_key=True, nullable=False)
    Description = db.Column(db.String(255), default=None)
    Typology = db.Column(db.String(100), default=None)
    Allergens = db.Column(db.String(255), default=None)
    ParentId = db.Column(db.String(100), db.ForeignKey('ProductCategory.ProductCategoryId'), default=None)

class ProductCategoryAllergens(db.Model):
    __tablename__ = 'ProductCategoryAllergens'
    ProductCategory = db.Column(db.String(100), db.ForeignKey('ProductCategory.ProductCategoryId'), primary_key=True, nullable=False)
    Allergens = db.Column(db.String(25), db.ForeignKey('Allergens.AllergenId'), primary_key=True, nullable=False)

class ProductClaims(db.Model):
    __tablename__ = 'ProductClaims'
    Product = db.Column(db.String(20), db.ForeignKey('Product.ProductId'), primary_key=True, nullable=False)
    Claims = db.Column(db.String(100), db.ForeignKey('Claims.ClaimsId'), primary_key=True, nullable=False)

class Claims(db.Model):
    __tablename__ = 'Claims'
    ClaimsId = db.Column(db.String(100), primary_key=True, nullable=False)
    Description = db.Column(db.Text, nullable=False)

class ProductDiet(db.Model):
    __tablename__ = 'ProductDiet'
    Product = db.Column(db.String(20), db.ForeignKey('Product.ProductId'), primary_key=True, nullable=False)
    Diet = db.Column(db.String(100), primary_key=True, nullable=False)

class ProductNutritionInfo(db.Model):
    __tablename__ = 'ProductNutritionInfo'
    Product = db.Column(db.String(20), db.ForeignKey('Product.ProductId'), primary_key=True, nullable=False)
    Nutrient = db.Column(db.String(20), db.ForeignKey('NutritionalInformation.NutrientId'), primary_key=True, nullable=False)
    NutrientValue = db.Column(db.Numeric(5, 2), default=None)

class Purchases(db.Model):
    __tablename__ = 'Purchases'
    PurchaseID = db.Column(db.String(20), primary_key=True, nullable=False)
    Date = db.Column(db.DateTime, default=None)
    Quantity = db.Column(db.Integer, default=None)
    Price = db.Column(db.Numeric(10, 2), default=None)
    Product = db.Column(db.String(20), db.ForeignKey('Product.ProductId'), primary_key=True, nullable=False)
    Family = db.Column(db.String(10), db.ForeignKey('Family.FamilyId'), default=None)

class Waste(db.Model):
    __tablename__ = 'Waste'
    Purchases = db.Column(db.String(20), db.ForeignKey('Purchases.PurchaseID'), primary_key=True, nullable=False)
    Date = db.Column(db.DateTime, default=None)
    Qty = db.Column(db.Float, default=None)
    Product = db.Column(db.String(20), primary_key=True, nullable=False)