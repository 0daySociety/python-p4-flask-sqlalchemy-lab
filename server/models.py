import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

try:
    db = SQLAlchemy(metadata=metadata)
except Exception as e:
    print("got this error", str(e))    

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeeper.id'))
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosure.id'))

class Zookeeper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date)
    animals = db.relationship('Animal', backref='zookeeper', lazy=True)

class Enclosure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String(100), nullable=False)
    open_to_visitors = db.Column(db.Boolean, default=False)
    animals = db.relationship('Animal', backref='enclosure', lazy=True)





