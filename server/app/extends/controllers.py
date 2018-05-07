from flask import Blueprint, render_template
from flask_restful import Api, Resource

register = Api(Blueprint(__name__, __name__, url_prefix="/extends"))

@register.route('/')
class Register(Resource):
    def get(self):
        return render_template('extends.html')