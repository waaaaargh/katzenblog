from unittest import TestCase
from base64 import b64encode
import json

import katzenblog

class ApiTestCase(TestCase):
    def open_authenticated(self, *args, **kwargs):
        return katzenblog.app.test_client().open( *args,
                headers={'Authorization': "Basic %s" % 
                          b64encode("%s:%s" % (self.username,
                                               self.password))},
                                                 **kwargs)
    
    def get_authenticated(self, *args, **kwargs):
        return self.open_authenticated(*args, method="GET", **kwargs)

    def post_authenticated(self, *args, **kwargs):
        return self.open_authenticated(*args, method="POST", **kwargs)
    
    def put_authenticated(self, *args, **kwargs):
        return self.open_authenticated(*args, method="PUT", **kwargs)
    
     
    def setUp(self):
        katzenblog.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        katzenblog.app.config['TESTING'] = True
        katzenblog.db.create_all()
        
        # create new User
        from katzenblog.model import User
        self.username = 'test'
        self.password = 'test'
        self.u = User(username=self.username,
                 email='test@example.com',
                 password=self.password,
                 screenname='test',
                 bio='test')
        katzenblog.db.session.add(self.u)
        katzenblog.db.session.commit()

    def test_http_auth(self):
        c = katzenblog.app.test_client()
        rv = c.get('/api/0/drafts')
        self.assertEqual(rv.status_code, 401)

        rv = self.open_authenticated('/api/0/drafts')
        self.assertEqual(rv.status_code, 200)
        
    def test_draft_lifecycle(self):
        rv = self.get_authenticated('/api/0/drafts')
        res = json.loads(rv.data)
        self.assertEqual(len(res), 0)
        
        rv = self.post_authenticated('/api/0/drafts', data={'title': "lel",
                                                            'text': "foo"})
        self.assertEqual(rv.status_code, 201)
        
        rv = self.get_authenticated('/api/0/drafts')
        res = json.loads(rv.data)
        self.assertEqual(len(res), 1)
        
        draft_id = res[0]["id"] 
        
        rv = self.get_authenticated("/api/0/drafts/%i" % draft_id)
        res = json.loads(rv.data)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(res["title"], 'lel')
        
        rv = self.put_authenticated("/api/0/drafts/%i" % draft_id, 
                                    data={'title': 'kek', 'text': 'bar'})
        self.assertEqual(rv.status_code, 204)

        rv = self.get_authenticated("/api/0/drafts/%i" % draft_id)
        res = json.loads(rv.data)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(res["title"], 'kek')
         
        rv = self.open_authenticated("/api/0/drafts/%i" % draft_id, method="DELETE")
        self.assertEqual(rv.status_code, 204)

        rv = self.get_authenticated('/api/0/drafts')
        res = json.loads(rv.data)
        self.assertEqual(len(res), 0)
     
    def tearDown(self):
        katzenblog.db.drop_all()
