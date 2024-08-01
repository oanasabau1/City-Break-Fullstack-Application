from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from marshmallow import Schema, fields, validate, ValidationError
import datetime
from config import db_url

app = Flask('City_Break_App')

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)

api = Api(app)


@app.route('/')
def index():
    return "The Flask Application starts here!"


def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, '%YYYY-%mm-%dd')
    except ValueError:
        raise ValidationError('Date must be in "YYYY-mm-dd" format.')


class EventSchema(Schema):
    city = fields.String(required=True, validate=validate.Length(min=1, max=128))
    date = fields.Date(required=True, format='%Y-%m-%d', validate=validate_date_format)
    title = fields.String(required=True, validate=validate.Length(min=1, max=128))
    description = fields.String(required=True, validate=validate.Length(min=1, max=128))
    address = fields.String(validate=validate.Length(max=128))
    category = fields.String(validate=validate.Length(max=128))
    price = fields.Float()


class WeatherSchema(Schema):
    city = fields.String(required=True, validate=validate.Length(min=1, max=128))
    date = fields.Date(required=True, format='%Y-%m-%d', validate=validate_date_format)
    temperature = fields.Integer(required=True, validate=validate.Range(min=-20, max=40,
                                                                        error="Temperature must be between -20 and 40 "
                                                                              "degrees Celsius"))
    humidity = fields.Integer(required=True, validate=validate.Range(min=0, max=100,
                                                                     error="Humidity must be between 0 and 100 percent"))
    description = fields.String(validate=validate.Length(max=128))


event_schema = EventSchema()
weather_schema = WeatherSchema()


class Events_Get_By_Filter(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date')

        if city and date:
            event = Event.query.filter_by(city=city, date=date).all()
        elif city:
            event = Event.query.filter_by(city=city).all()
        elif date:
            event = Event.query.filter_by(date=date).all()
        else:
            return jsonify({'message': 'Please provide city and date'})

        fetched_events = [e.to_dict() for e in event]
        if fetched_events:
            return jsonify({'events': fetched_events})
        else:
            return jsonify({'message': 'No events found match the given criteria'})


class Events_Post(Resource):
    def post(self):
        data = request.json
        try:
            validated_data = event_schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        new_event = Event(
            city=validated_data['city'],
            date=validated_data['date'],
            title=validated_data['title'],
            description=validated_data['description'],
            address=validated_data.get('address'),
            category=validated_data.get('category'),
            price=validated_data.get('price')
        )
        db.session.add(new_event)
        db.session.commit()
        return 'Event added', 200


class Events_Put(Resource):
    def put(self):
        event_id = request.args.get('id')
        event = Event.query.get_or_404(event_id)
        data = request.json
        try:
            validated_data = event_schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        event.city = validated_data['city']
        event.date = validated_data['date']
        event.title = validated_data['title']
        event.description = validated_data['description']
        event.address = validated_data.get('address')
        event.category = validated_data.get('category')
        event.price = validated_data.get('price')
        db.session.commit()
        return 'Event updated successfully!', 200


class Events_Delete(Resource):
    def delete(self):
        event_id = request.args.get('id')
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return 'Event deleted successfully!', 200


class Weathers_Get_By_Filter(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date')

        if city and date:
            weather = Weather.query.filter_by(city=city, date=date).all()
        elif city:
            weather = Weather.query.filter_by(city=city).all()
        elif date:
            weather = Weather.query.filter_by(date=date).all()
        else:
            return jsonify({'message': 'Please provide city and date'})

        fetched_weather = [w.to_dict() for w in weather]
        if fetched_weather:
            return jsonify({'weather': fetched_weather})
        else:
            return jsonify({'message': 'No weather found match the given criteria'})


class Weathers_Post(Resource):
    def post(self):
        data = request.json
        try:
            validated_data = weather_schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        new_weather = Weather(
            city=validated_data['city'],
            date=validated_data['date'],
            temperature=validated_data['temperature'],
            humidity=validated_data['humidity'],
            description=validated_data['description'],
        )
        db.session.add(new_weather)
        db.session.commit()
        return 'Weather added successfully!', 200


class Weathers_Put(Resource):
    def put(self):
        weather_id = request.args.get('id')
        weather = Weather.query.get_or_404(weather_id)
        data = request.json
        try:
            validated_data = weather_schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        weather.city = validated_data['city']
        weather.date = validated_data['date']
        weather.temperature = validated_data['temperature']
        weather.humidity = validated_data['humidity']
        weather.description = validated_data['description']
        db.session.commit()
        return 'Weather updated successfully!', 200


class Weathers_Delete(Resource):
    def delete(self):
        weather_id = request.args.get('id')
        weather = Weather.query.get_or_404(weather_id)
        db.session.delete(weather)
        db.session.commit()
        return 'Weather deleted', 200


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
            'city': self.city,
            'date': self.date.strftime('%Y-%m-%d'),
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
            'city': self.city,
            'date': self.date.strftime('%Y-%m-%d'),
            'temperature': self.temperature,
            'humidity': self.humidity,
            'description': self.description
        }


api.add_resource(Events_Get_By_Filter, '/events')
api.add_resource(Events_Post, '/events/add')
api.add_resource(Events_Put, '/events/update')
api.add_resource(Events_Delete, '/events/delete')

api.add_resource(Weathers_Get_By_Filter, '/weather')
api.add_resource(Weathers_Post, '/weather/add')
api.add_resource(Weathers_Put, '/weather/update')
api.add_resource(Weathers_Delete, '/weather/delete')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
