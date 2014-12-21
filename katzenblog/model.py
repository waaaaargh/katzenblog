from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from katzenblog import db
from katzenblog.util import slugify

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    passwordhash = db.Column(db.String)
    email = db.Column(db.String)
    
    screenname = db.Column(db.String)
    bio = db.Column(db.String)
    
    def __init__(self, username, email, password, screenname, bio):
        self.username = username
        self.email = email
        self.screenname = screenname
        self.bio = bio
        
        self.passwordhash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)
    
    def set_password(self, password):
        self.passwordhash = generate_password_hash(password)
        
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    def __init__(self, name):
        self.name = name
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    text = db.Column(db.String)
    slug = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    last_edit_time = db.Column(db.DateTime)
    
    owner = db.relationship('User', backref=db.backref('posts', 
                                                       lazy='dynamic'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    category = db.relationship('Category', backref=db.backref('posts',
                                                              lazy='dynamic'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, title, text, owner):
        self.title = title
        self.text = text
        self.owner = owner
        
        self.slug = slugify(title)
        
        self.create_time = datetime.now()
        self.last_edit_time = datetime.now()
    
    def edit(self, title, text):
        self.title = title
        self.text = text
 
        self.slug = slugify(title)

        self.last_edit_time = datetime.now()
