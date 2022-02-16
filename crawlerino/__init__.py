from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# DATABASE PARAMS
db = SQLAlchemy()
DB_NAME = "databaserino.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisisasecretkey' # cookies/session variables encryption
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    """ Establish application routes """
    from .homepage import homepage

    """ Establish application blueprints """
    app.register_blueprint(homepage, url_prefix='/')

    """ Establish database structure """
    from .models import tablerino

    """ Call create_database() """
    create_database(app)

    return app
        
def create_database(app):
    if not path.exists('crawlerino/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')