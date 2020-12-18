from recipe_scheduler.config import Config
from flask import Flask
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_msearch import Search
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def admin_control(app):
    from recipe_scheduler.admincc.admincontrol import (
        MyAdminIndexView, MyModelView)
    from recipe_scheduler.models import (
        User, Group, Event, Recipe, Category, Role)
    adminCC = Admin(app, index_view=MyAdminIndexView())
    adminCC.add_view(MyModelView(User, db.session))
    adminCC.add_view(MyModelView(Group, db.session))
    adminCC.add_view(MyModelView(Event, db.session))
    adminCC.add_view(MyModelView(Recipe, db.session))
    adminCC.add_view(MyModelView(Category, db.session))
    adminCC.add_view(MyModelView(Role, db.session))


def create_app(config_class=Config):
    """
    Initiate application and register the routes and handlers to blueprint
    :param config_class: setting for sql
    :return: application initiate and blueprint mapping
    """
    app = Flask(__name__)

    app.config.from_object(config_class)
    search = Search()
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    search.init_app(app)
    mail.init_app(app)

    from recipe_scheduler.main.routes import main
    from recipe_scheduler.categories.routes import categories
    from recipe_scheduler.events.routes import events
    from recipe_scheduler.users.routes import users
    from recipe_scheduler.sub.routes import sub
    from recipe_scheduler.uploads.routes import uploads
    from recipe_scheduler.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(categories)
    app.register_blueprint(events)
    app.register_blueprint(users)
    app.register_blueprint(sub)
    app.register_blueprint(uploads)
    app.register_blueprint(errors)

    admin_control(app)

    return app
