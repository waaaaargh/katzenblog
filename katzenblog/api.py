from flask.ext.restful import Resource

from katzenblog import api
from katzenblog.model import Post, User

from katzenblog.auth import requires_auth

class PostsResource(Resource):
    def get(self):
        return [ { "id": p.id,
                   "title": p.title, 
                   "text": p.text,
                   "owner": { "id": p.owner.id,
                              "username": p.owner.username,
                              "screenname": p.owner.screenname },
                   "create_time": p.create_time.isoformat(),
                   "last_edited_on": p.last_edit_time.isoformat() } for p in Post.query.all() ]
api.add_resource(PostsResource, 'posts')

class UserResource(Resource):
    @requires_auth
    def get(self, auth_username):
        u = User.query.filter(User.username==auth_username).one()
        return { "id": u.id,
                 "username": u.username,
                 "screenname": u.screenname,
                 "bio": u.bio }
api.add_resource(UserResource, 'user')
