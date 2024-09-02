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
    Family = db.Column(db.String(45), db.ForeignKey('Family.FamilyId'), nullable=True)
    Role = db.Column(db.String(45), nullable=True)
    Address = db.Column(db.String(45), nullable=True)
    Age = db.Column(db.Integer, nullable=True)
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

    Consumer = db.Column(db.String(45), db.ForeignKey('Consumer.ConsumerId'), primary_key=True, nullable=False)
    Date = db.Column(db.DateTime, primary_key=True, nullable=False)
    Weight = db.Column(db.Numeric(5, 2), nullable=True)
    Height = db.Column(db.Numeric(5, 1), nullable=True)


class Family(db.Model):
    __tablename__ = 'Family'

    FamilyId = db.Column(db.Integer, primary_key=True, nullable=False)
    Description = db.Column(db.String(255), nullable=True)
    Members = db.Column(db.Integer, nullable=True)
