# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

from flask import Flask

app = Flask(__name__)

def randomExtend(id, pw, room, time):
    from api.dms import applyExtension, getExtensionMaps

    maps = getExtensionMaps(room)
    
    for seat in maps:
        if isinstance(seat, int):
            res = applyExtension(id, pw, room, seat, time)
            print(seat, id)
            if res:
                return "Success", 200

    return "Failed", 403

@app.route('/auto/dms/extend')
def extend():
    from api.dms import applyExtension
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
                randomExtend(id, pw, room, time)
        
        if extend_twelve:
            print('twelve', id, room, seat)
            if not applyExtension(id, pw, room, seat, time=12):
                randomExtend(id, pw, room, time)

    return "End", 200
    
@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]