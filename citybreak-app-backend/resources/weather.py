from flask_restful import Resource
from flask import request
from models import db, Weather
from schemas import WeatherSchema
from marshmallow import ValidationError

weather_schema = WeatherSchema()


class Weathers_Get(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date')
        weathers = db.session.query(Weather)
        if city:
            weathers = weathers.filter(Weather.city == city)
        if date:
            weathers = weathers.filter(Weather.date == date)
        return [w.to_dict() for w in weathers.all()], 200


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
        return 'Weather added successfully!', 201


import logging

class Weathers_Put(Resource):
    def put(self):
        weather_id = request.args.get('id')
        weather = Weather.query.get_or_404(weather_id)
        data = request.json
        logging.debug(f'Received data: {data}')
        try:
            validated_data = weather_schema.load(data)
        except ValidationError as err:
            logging.error(f'Validation error: {err.messages}')
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
        return 'Weather deleted successfully!', 200
