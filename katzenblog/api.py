from flask.ext.restful import Resource

from katzenblog import api, db
from katzenblog.model import Post

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
