from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Consumer(db.Model):
    __tablename__ = 'consumer'

    ConsumerId = db.Column(db.Integer, autoincrement=True, unique=True, index=True, primary_key=True, nullable=False)
    Email = db.Column(db.String(45), nullable=False, unique=True)
    PasswordHash = db.Column(db.String(255), nullable=False)
    Name = db.Column(db.String(45), nullable=False)
    Surname = db.Column(db.String(45), nullable=True)
    DateOfBirth = db.Column(db.Date, nullable=False)
    PlaceOfBirth = db.Column(db.String(45), nullable=True)
    Gender = db.Column(db.Enum('male', 'female', name='enum_gender'), nullable=False)
    Family = db.Column(db.String(45), nullable=True)
    Role = db.Column(db.String(45), nullable=True)
    Address = db.Column(db.String(45), nullable=True)
    Age = db.Column(db.Integer, nullable=True)
    FamilyId = db.Column(db.String(45), db.ForeignKey('family.FamilyId'), nullable=True)
    body_compositions = db.relationship('BodyComposition', backref="consumer", lazy=True)


class BodyComposition(db.Model):
    __tablename__ = 'body_composition'

    Consumer = db.Column(db.String(45), db.ForeignKey('consumer.ConsumerId'), primary_key=True, nullable=False)
    Date = db.Column(db.DateTime, primary_key=True, nullable=False)
    Weight = db.Column(db.Numeric(5, 2), nullable=True)
    Height = db.Column(db.Numeric(5, 1), nullable=True)


class Family(db.Model):
    __tablename__ = 'family'

    FamilyId = db.Column(db.Integer, primary_key=True, nullable=False)
    Description = db.Column(db.String(255), nullable=True)
    Members = db.Column(db.Integer, nullable=True)

    # ...