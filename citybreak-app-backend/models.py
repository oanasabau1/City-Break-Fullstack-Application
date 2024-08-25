from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    date = db.Column(db.Date)
    title = db.Column(db.String(128))
    description = db.Column(db.String(128))
    address = db.Column(db.String(128))
    category = db.Column(db.String(128))
    price = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'date': self.date.strftime('%Y-%m-%d') if self.date else datetime.today().strftime('%Y-%m-%d'),
            'title': self.title,
            'description': self.description,
            'address': self.address,
            'category': self.category,
            'price': self.price
        }


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    date = db.Column(db.Date)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    description = db.Column(db.String(128))

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'date': self.date.strftime('%Y-%m-%d') if self.date else datetime.today().strftime('%Y-%m-%d'),
            'temperature': self.temperature,
            'humidity': self.humidity,
            'description': self.description
        }
