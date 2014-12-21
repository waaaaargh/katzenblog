from flask.ext.restful import Resource

from katzenblog import api
from katzenblog.model import Post, User, Category

from katzenblog.auth import requires_auth

class PublicPostsResource(Resource):
    def get(self):
        return [ { "id": p.id,
                   "title": p.title, 
                   "text": p.text,
                   "owner": { "id": p.owner.id,
                              "username": p.owner.username,
                              "screenname": p.owner.screenname },
                   "create_time": p.create_time.isoformat(),
                   "last_edited_on": p.last_edit_time.isoformat() } for p in Post.query.all() ]
api.add_resource(PublicPostsResource, 'posts')

class PublicUserResource(Resource):
    def get(self):
        return [ { "id": u.id,
                   "username": u.username,
                   "screenname": u.screenname,
                   "bio": u.bio } for u in User.query.all() ]
api.add_resource(PublicUserResource, 'user')

class PublicCategoryResource(Resource):
    def get(self):
        return [ { "id": c.id,
                   "title": c.name } for c in Category.query.all() ]
api.add_resource(PublicCategoryResource, 'category')
