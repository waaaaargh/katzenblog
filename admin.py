#!/usr/bin/env python2

from flask.ext.script import Manager

from katzenblog import app

manager = Manager(app)

@manager.command
def run_tests():
    from tests import *
    import unittest
    unittest.main()

if __name__ == '__main__':
    manager.run()
