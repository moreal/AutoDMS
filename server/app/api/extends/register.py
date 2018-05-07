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

        # Check it exists already on the gcloud datastore
        from google.cloud import datastore

        client = datastore.Client()
        client.query(kind="", namespace)

        class_num = int(request.form['class_num'])
        seat_num = int(request.form['seat_num'])

        extend_eleven = request.form['eleven']
        extend_twelve = request.form['twelve']