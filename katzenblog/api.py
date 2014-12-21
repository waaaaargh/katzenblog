from flask import redirect
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import RequestParser
from sqlalchemy.orm.exc import NoResultFound

from katzenblog import api, db
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
                   "last_edit_time": p.last_edit_time.isoformat() } for p in Post.query.all() ]
api.add_resource(PublicPostsResource, 'post')

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

class DraftResource(Resource):
    @requires_auth
    def get(self, auth_username):
        u = User.query.filter(User.username == auth_username).one()
        
        drafts = Post.query.filter(Post.owner == u).filter(Post.published == False).all()
        
        return [ { "id": d.id,
                   "title": d.title,
                   "text": d.text,
                   "create_time": d.create_time.isoformat(),
                   "last_edit_time": d.last_edit_time.isoformat() } for d in drafts ]
    
    @requires_auth
    def post(self, auth_username):
        u = User.query.filter(User.username == auth_username).one()

        parser = RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('text', type=str, required=True)
        args = parser.parse_args()
        
        p = Post(title=args.title,
                 text=args.text,
                 owner=u)
        p.published = False
        db.session.add(p)
        db.session.commit()
        
        return redirect("/api/0/drafts/%i" % p.id, 201)
api.add_resource(DraftResource, 'drafts')

class SingleDraftResource(Resource):
    @requires_auth
    def get(self, draft_id, auth_username):
        d = Post.query.filter(Post.id == draft_id).one()
        return { "id": d.id,
                 "title": d.title, 
                 "text": d.text,
                 "create_time": d.create_time.isoformat(),
                 "last_edit_time": d.last_edit_time.isoformat(),
                 "published": d.published }
    
    @requires_auth
    def delete(self, draft_id, auth_username):
        try:
            d = Post.query.filter(Post.id == draft_id).one()
        except NoResultFound:
            return None, 404
        db.session.delete(d)
        db.session.commit()
        return None, 204

    @requires_auth
    def put(self, draft_id, auth_username):
        parser = RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('text', type=str, required=True)
        args = parser.parse_args()
        
        try:
            p = Post.query.filter(Post.id == draft_id).one()
        except NoResultFound:
            return None, 404
            
        p.edit(args.title, args.text)

        db.session.commit()
        return None, 204
api.add_resource(SingleDraftResource, 'drafts/<int:draft_id>')
