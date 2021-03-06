from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_jsglue import JSGlue
from flask_session import Session
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object('config')

jsglue = JSGlue(app)

Session(app)
db = SQLAlchemy(app, session_options={"autoflush": True})

admin = Admin(app, name='usomix', template_mode='bootstrap3')

from application import views, models, forms, helpers
from application.views import admin
#from .views.main import main
#app.register_blueprint(main, url_prefix='/main')



helpers.env.globals['session'] = views.session

# ensure responses aren't cached
#if app.config["DEBUG"]:
#    @app.after_request
#    def after_request(response):
#        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#        response.headers["Expires"] = 0
#        response.headers["Pragma"] = "no-cache"
#        return response


# configure session to use filesystem (instead of signed cookies)