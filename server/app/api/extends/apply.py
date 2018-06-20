from flask import request, Blueprint
from flask import render_template, redirect
from flask_restful import Api, Resource

import _thread

api = Api(Blueprint(__name__, __name__, url_prefix='/api/extend'))

def apply():
    from api.dms import applyExtension, randomExtend
    from google.cloud import datastore as ds
    
    client = ds.Client.from_service_account_json("service_account.json")
    students = list(client.query(namespace="AutoDMS", kind="Students").fetch())

    for student in students:
        id = student['id']
        pw = student['pw']
        room = student['room']
        seat = student['seat']

        extend_eleven = student['extend_eleven']
        extend_twelve = student['extend_twelve']

        if extend_eleven:
            print('eleven', id, room, seat)
            if not applyExtension(id, pw, room, seat, time=11):
                randomExtend(id, pw, room, 11)
        
        if extend_twelve:
            print('twelve', id, room, seat)
            if not applyExtension(id, pw, room, seat, time=12):
                randomExtend(id, pw, room, 12)

    return "End", 200

@api.resource('/apply')
class Apply(Resource):
    def post(self):
        _thread.start_new_thread(apply, ())
        return "End", 200