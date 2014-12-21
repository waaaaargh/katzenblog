#!/usr/bin/env python2

from flask.ext.script import Manager

from katzenblog import app, db

manager = Manager(app)

@manager.command
def create_db():
    db.create_all()

if __name__ == '__main__':
    manager.run()
