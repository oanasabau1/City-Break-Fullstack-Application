from flask import Flask
from flask_restful import Api
from models import db
from config import db_url
from resources.events import Events_Get, Events_Post, Events_Put, Events_Delete
from resources.weather import Weathers_Get, Weathers_Post, Weathers_Put, Weathers_Delete

app = Flask('City_Break_App')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

db.init_app(app)
api = Api(app)


@app.route('/')
def index():
    return "The Flask Application starts here!"


api.add_resource(Events_Get, '/events')
api.add_resource(Events_Post, '/events/add')
api.add_resource(Events_Put, '/events/update')
api.add_resource(Events_Delete, '/events/delete')

api.add_resource(Weathers_Get, '/weather')
api.add_resource(Weathers_Post, '/weather/add')
api.add_resource(Weathers_Put, '/weather/update')
api.add_resource(Weathers_Delete, '/weather/delete')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
