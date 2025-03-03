from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)  # Ensure 'phone' exists
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(30), default=lambda: datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))  
    # date = db.Column(db.String(10), default=lambda: datetime.now().strftime("%Y-%m-%d"))  # Stores only the date
    # time = db.Column(db.String(10), default=lambda: datetime.now().strftime("%I:%M:%S %p"))  # Stores only the time in 12-hour format

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
# class Image(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(255), nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
