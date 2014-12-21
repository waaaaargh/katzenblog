#!/usr/bin/env python2
import sys

from flask.ext.script import Manager

from katzenblog import app, db

manager = Manager(app)

@manager.command
def create_db():
    db.create_all()
    
@manager.command
def add_user(username):
    from katzenblog.model import User
    from getpass import getpass
    from sqlalchemy.exc import OperationalError

    print("[i] adding user %s" % username)
    password = ''
    while True:
        try1 = getpass("Password:")
        try2 = getpass("Password (Repeat):")
        if try1 == try2:
            password = try1
            break
    
    u = User(username=username,
             password=password,
             email='',
             screenname='',
             bio='')
    
    db.session.add(u)
    try:
        db.session.commit()
    except OperationalError:
        print("[e] Couldn't add user; did you run `create_db` yet?")
        sys.exit(1)

    print("[i] Done adding user %s" % username)

if __name__ == '__main__':
    manager.run()
