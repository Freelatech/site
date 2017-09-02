#from application import app,db
#from flask import Blueprint, render_template, abort
#from jinja2 import TemplateNotFound
#from flask_admin.contrib.sqla import ModelView
#from application.models import Auth, Classe, Educ, Experiencia, Cert, Horario, Prestador, Subclasse, Sugestao, Suporte, User
#from flask_admin import Admin

admin = Admin(app, name='usomix', template_mode='bootstrap3')
"""admin.add_view(ModelView(Auth, db.session))
admin.add_view(ModelView(Classe, db.session))
admin.add_view(ModelView(Educ, db.session))
admin.add_view(ModelView(Experiencia, db.session))
admin.add_view(ModelView(Cert, db.session))
admin.add_view(ModelView(Horario, db.session))
admin.add_view(ModelView(Prestador, db.session))
admin.add_view(ModelView(Subclasse, db.session))
admin.add_view(ModelView(Sugestao, db.session))
admin.add_view(ModelView(Suporte, db.session))
admin.add_view(ModelView(User, db.session))"""

#@admin.route('/', defaults={'page': 'index'})
#@admin.route('/<page>')
#def show(page):
#    return render_template('index.html')