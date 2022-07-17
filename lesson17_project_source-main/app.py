from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}

    db.init_app(app)

    with app.app_context():

        api = Api(app)
        app.config['api'] = api

        import routes

        return app
