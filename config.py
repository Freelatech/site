import os
from tempfile import mkdtemp
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SESSION_FILE_DIR = mkdtemp()
SESSION_PERMANENT = True
SESSION_TYPE = "filesystem"
JSON_SORT_KEYS = False