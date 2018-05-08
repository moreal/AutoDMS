from flask import Blueprint, render_template
from flask_restful import Api, Resource

api = Api(Blueprint(__name__, __name__, url_prefix="/extends"))

@api.resource('/')
class Extend(Resource):
    def get(self):
        return render_template('extends.html')