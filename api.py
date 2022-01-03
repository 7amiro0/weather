"""This file create API."""

from flask import Flask
from flask_restful import Resource, Api, reqparse
import db

app = Flask('__name__')
api = Api(app)

class CityName(Resource):
    """Return list city."""
    def get(self):
        """Return list city."""
        return db.city_name()

class Params(Resource):
    """Return value city."""
    def get(self):
        """Return value city."""
        parses = reqparse.RequestParser()
        parses.add_argument('value_type', required=True)
        parses.add_argument('city', required=True)
        args = parses.parse_args()
        return db.params(args)

class Record(Resource):
    """Return value city in days."""
    def get(self):
        """Return value cite in days."""
        parser = reqparse.RequestParser()
        parser.add_argument('city', required=True)
        parser.add_argument('start_dt', required=True)
        parser.add_argument('end_dt', required=True)
        args = parser.parse_args()
        return db.record(args)

class MovingMean(Resource):
    """Return midle value city all days."""
    def get(self):
        """Return midle value city all days."""
        parser= reqparse.RequestParser()
        parser.add_argument('value_type', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()
        return db.moving_average(args)

api.add_resource(CityName, '/cities')
api.add_resource(Params, '/mean')
api.add_resource(Record, '/records')
api.add_resource(MovingMean, '/moving_mean')
app.run(debug=True)
