from flask import request, Blueprint
from flask_restful import Api, Resource

api = Api(Blueprint(__name__, __name__, url_prefix='/api/register'))

@api.resource('/extend')
class Register(Resource):
    def post(self):
        # Extract form variables
        id = request.form['id']
        pw = request.form['pw']

        # Check isRight Id and Pw
        import requests
        
        resp = requests.post("http://dms.istruly.sexy/auth", data={"id": id, "pw": pw})

        if resp.status_code is not 200:
            return '', 403

        class_num = int(request.form['class_num'])
        seat_num = int(request.form['seat_num'])

        extend_eleven = request.form['eleven'] if 'eleven' in request.form else None
        extend_twelve = request.form['twelve'] if 'twelve' in request.form else None

        print(extend_eleven, extend_twelve)

        # Get Access Token and Refresh Token from login data
        # import json
        
        # data = json.loads(resp.text)
        # access_token = data['access_token']
        # refresh_token = data['refresh_token']

        # Prepare Client for datastore
        from google.auth import compute_engine
        from google.cloud import datastore

        client = datastore.Client(project="i-like-dsmproject", credentials=compute_engine.Credentials())

        # Check duplicate seat
        def isDuplicate(prop):
            query = client.query(namespace="AutoDMS", kind="Students")
            query.add_filter('seat', '=', seat_num)
            query.add_filter('room', '=', class_num)
            query.add_filter(prop, '=', True)
            return len(list(query.fetch())) is not 0

        if extend_eleven is "on":
            if isDuplicate('extend_eleven'):
                return "Duplicate Seat", 403
        
        if extend_twelve is "on":
            if isDuplicate('extend_twelve'):
                return "Duplicate Seat", 403

        # Upsert
        key = client.key('Students', id, namespace="AutoDMS")
        task = datastore.Entity(key=key)

        task.update({
            "id": id,
            "pw": pw,
            "room": class_num,
            "seat": seat_num,
            "extend_eleven": extend_eleven is "on",
            "extend_twelve": extend_twelve is "on",
        })

        client.put(task)

        return "Good Return", 201