from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('application', 'templates'))

from application.views import session, request, url_for, redirect, app, db
from functools import wraps
from flask_mail import Mail, Message
from application.models import Auth, Classe, Educ, Experiencia, Cert, Horario, Prestador, Subclasse, Sugestao, Suporte, User

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

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], urlfoto=login_session['picture'])
    db.session.add(newUser)
    session.commit()
    user = User.query.filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = User.query.filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = User.query.filter_by(email=email).one()
        return user.id
    except:
        return None


