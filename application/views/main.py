from application import app, db
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
import json
from collections import OrderedDict
#from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView
from passlib.apps import custom_app_context as pwd_context
from application.helpers import env, login_required
from application.models import Auth, Classe, Educ, Experiencia, Cert, Horario, Prestador, Subclasse, Sugestao, Suporte, User

main = Blueprint('main', __name__,
                        template_folder='templates')

#admin = Admin(app, name='usomix', template_mode='bootstrap3')
#admin.add_view(ModelView(Agendamento, db.session))
#admin.add_view(ModelView(Auth, db.session))
#admin.add_view(ModelView(Classe, db.session))
#admin.add_view(ModelView(Opfin, db.session))
#admin.add_view(ModelView(Service, db.session))
#admin.add_view(ModelView(Subclasse, db.session))
#admin.add_view(ModelView(Transaction, db.session))
#admin.add_view(ModelView(User, db.session))

@main.route("/")
def teste():
    return render_template("index.html")
