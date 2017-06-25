from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('application', 'templates'))

from application.views import session, request, url_for, redirect, app
from functools import wraps
from flask_mail import Mail, Message

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
           return redirect(url_for("entrar", dest=request.endpoint))
        return f(*args, **kwargs)
    return decorated_function
    
def adm_login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("adm_id") is None:
           return redirect(url_for("adm_login", next=request.endpoint))
        return f(*args, **kwargs)
    return decorated_function



