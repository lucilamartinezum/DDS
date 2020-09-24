import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_apscheduler import APScheduler

ma = Marshmallow()

api = Api()
scheduler = APScheduler()
db = SQLAlchemy()
jwt = JWTManager()
mailsender = Mail()

class Config(object):
    SCHEDULER_JOBSTORES = {'default':SQLAlchemyJobStore(url='sqlite:///'+str(os.getenv('SQLALCHEMY_DATABASE_PATH'))+str(os.getenv('SQLALCHEMY_DATABASE_NAME')))}
    SCHEDULER_API_ENABLED = True


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    load_dotenv()
    if not os.path.exists(os.getenv('SQLALCHEMY_DATABASE_PATH')+os.getenv('SQLALCHEMY_DATABASE_NAME')):
        os.mknod(os.getenv('SQLALCHEMY_DATABASE_PATH')+os.getenv('SQLALCHEMY_DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('SQLALCHEMY_DATABASE_PATH')+os.getenv('SQLALCHEMY_DATABASE_NAME')


    db.init_app(app)
    ma.init_app(app)
    app.config['JWT_SECRET_KEY'] = 'programacion12020'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
    jwt.init_app(app)

    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        def activatePrimaryKeys(conection, conection_record):
            conection.execute('pragma foreign_keys=ON')

        with app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', activatePrimaryKeys)

    import main.resources as resources
    api.add_resource(resources.SensorsResource, '/sensors')
    api.add_resource(resources.SensorResource, '/sensor/<id>')

    api.add_resource(resources.VerifiedseismsResource, '/verified-seisms')
    api.add_resource(resources.VerifiedseismResource, '/verified-seism/<id>')

    api.add_resource(resources.UnverifiedseismsResource, '/unverified-seisms')
    api.add_resource(resources.UnverifiedseismResource, '/unverified-seism/<id>')

    api.add_resource(resources.UsersResource, '/users')
    api.add_resource(resources.UserResource, '/user/<id>', endpoint='user_id')
    api.init_app(app)

    scheduler.init_app(app)
    scheduler.start()

    @app.before_first_request
    def load_tasks():
        from main.services import tasks

    from main.auth import routes
    import main.resources as resources

    app.register_blueprint(auth.routes.auth)

    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    mailsender.init_app(app)

    return app