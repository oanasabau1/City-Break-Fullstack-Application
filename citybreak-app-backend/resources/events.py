from flask_restful import Resource
from flask import request
from models import db, Event
from schemas import EventSchema
from marshmallow import ValidationError

event_schema = EventSchema()


class Events_Get(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date')
        events = db.session.query(Event)
        if city:
            events = events.filter(Event.city == city)
        if date:
            events = events.filter(Event.date == date)
        return [e.to_dict() for e in events.all()], 200


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
        return 'Event added successfully!', 201


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
