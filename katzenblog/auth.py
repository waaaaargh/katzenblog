# blatantly stolen from:
#   http://flask.pocoo.org/snippets/8/

from functools import wraps
from flask import request, Response

from sqlalchemy.orm.exc import NoResultFound

from katzenblog import User

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    try:
        u = User.query.filter(username == username).one()
    except NoResultFound:
        return False
    
    return u.check_password(password)
    

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, auth_username=auth.username, **kwargs)
    return decorated
