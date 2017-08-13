from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask_admin.contrib.sqla import ModelView

admin = Blueprint('admin', __name__,
                        template_folder='templates')

@admin.route('/', defaults={'page': 'index'})
@admin.route('/<page>')
def show(page):
    return render_template('index.html')