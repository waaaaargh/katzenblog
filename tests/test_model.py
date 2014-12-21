from unittest import TestCase

from katzenblog import app, db
from katzenblog.model import User, Post, Category

class TestModelUser(TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

        self.u = User(username='test',
                 password='test',
                 email='test@test.com',
                 screenname='Maria Musterfrau',
                 bio='asdf')
        
    def test_model_user(self):
        db.session.add(self.u)
        db.session.commit()
        
        v = User.query.all()[0]
        self.assertEqual(v.username, self.u.username)
        self.assertIsNotNone(v.id)
        
    def tearDown(self):
        db.drop_all()
        
class TestModelPost(TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

        u = User(username='test',
                 password='test',
                 email='test@test.com',
                 screenname='Maria Musterfrau',
                 bio='asdf')
        db.session.add(u)
        db.session.commit()
        
    def test_model_post(self):
        u = User.query.all()[0]
        p = Post(title="Test",
                 text="Lelelelelelelele",
                 owner=u)
        db.session.add(p)
        db.session.commit()
        
        q = Post.query.all()[0]
        self.assertEqual(p.id, q.id)
        self.assertEqual(q.owner.id, q.id)
        self.assertNotEqual(u.posts, [])

    def tearDown(self):
        db.drop_all()
     
class TestModelCategory(TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

        u = User(username='test',
                 password='test',
                 email='test@test.com',
                 screenname='Maria Musterfrau',
                 bio='asdf')
        db.session.add(u)
        p = Post(title="Test",
                 text="Lelelelelelelele",
                 owner=u)
        db.session.add(p)
        db.session.commit()
          
    def test_model_category(self):
        c = Category('topkek')
        
        p = Post.query.all()[0]

        p.category = c

        db.session.add(c)
        db.session.add(p)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
