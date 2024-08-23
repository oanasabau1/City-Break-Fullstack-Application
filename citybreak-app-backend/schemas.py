from marshmallow import Schema, fields, validate, ValidationError
import datetime


class EventSchema(Schema):
    city = fields.String(required=True, validate=validate.Length(min=1, max=128))
    date = fields.Date(required=True, format='%Y-%m-%d')
    title = fields.String(required=True, validate=validate.Length(min=1, max=128))
    description = fields.String(required=True, validate=validate.Length(min=1, max=128))
    address = fields.String(validate=validate.Length(max=128))
    category = fields.String(validate=validate.Length(max=128))
    price = fields.Float()


class WeatherSchema(Schema):
    city = fields.String(required=True, validate=validate.Length(min=1, max=128))
    date = fields.Date(required=True, format='%Y-%m-%d')
    temperature = fields.Integer(required=True, validate=validate.Range(min=-20, max=40,
                                                                        error="Temperature must be between -20 and 40 "
                                                                              "degrees Celsius"))
    humidity = fields.Integer(required=True, validate=validate.Range(min=0, max=100,
                                                                     error="Humidity must be between 0 and 100 percent"))
    description = fields.String(validate=validate.Length(max=128))
