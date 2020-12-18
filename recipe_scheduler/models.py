"""
Model
"""
from flask import current_app
from flask_login import UserMixin
from recipe_scheduler import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def loader_user(user_id):
    """
    To get the user information when the login.
    :param user_id: login user_id
    :return: login user_id
    """
    return User.query.get(int(user_id))


user_groups = db.Table(
    'user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class User(db.Model, UserMixin):
    """
    User models for user information
    """
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_groups = db.relationship('Group', secondary='user_groups',
                                  backref=db.backref('users', lazy='dynamic'))
    roles = db.relationship('Role', secondary='users_roles',
                                  backref=db.backref('users', lazy='dynamic'))
    current_group = db.Column(db.Integer)
    groups = db.relationship('Group', backref='groups', lazy=True)

    def __init__(self, email=None, password=None, current_group=None):
        self.email = email
        self.password = password
        self.current_group = current_group

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'user_groups': [Group.to_dict(c) for c in self.user_groups]
        }

    def update_current_group(self, select_group):
        self.current_group = select_group

    def get_current_group(self):
        return self.current_group

    def is_admin(self):
        return self.roles[0].role_name == 'admin'


class Role(db.Model):
    """
    Group model
    """
    __table_name__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=False)

    def to_dict(self):
        return {
            'id': self.id,
            'role_name': self.role_name
        }


class Group(db.Model):
    """
    Group model
    """
    __table_name__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), unique=False)
    events = db.relationship('Event', backref='event_group', lazy=True)
    categories = db.relationship(
        'Category', backref='category_group', lazy=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_reset_token(self, expires_sec=1800):
        """
        To generate the token with secret_key
        :param expires_sec: expire time for token. second
        :return: token
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'group_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        To verify if the user is in the database with the token
        :param token: token is provided by get_reset_token()
        :return: user information
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            group_id = s.loads(token)['group_id']
            return Group.query.get(group_id)
        # except:
        except:
            return None
        # return Group.query.get(group_id)

    def to_dict(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
            'events': self.events,
            'categories': self.categories,
            'created_by': self.created_by
        }


class Recipe(db.Model):
    """
    Recipe Model
    """
    __table_name__ = 'recipe'
    __searchable__ = ['recipe_name', 'description']
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100), unique=False, nullable=False)
    recipe_url = db.Column(db.String(2083), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    events = db.relationship(
        'Event', backref='recipe', lazy=True, cascade="all")

    def to_dict(self):
        return {
            'id': self.id,
            'recipe_name': self.recipe_name,
            'recipe_url': self.recipe_url,
            'description': self.description,
            'category_id': self.category_id,
            'events': self.events
        }


class Category(db.Model):
    """
    Category Model
    """
    __table_name__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(30), unique=False, nullable=False)
    recipes = db.relationship('Recipe', backref='category', lazy=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'categories': self.recipes
        }


class Event(db.Model):
    """
    Event model
    """
    __table_name__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    event_date = db.Column(db.Date, nullable=False)
    event_type = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.id', ondelete="CASCADE"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'event_date': self.event_date,
            'event_type': self.event_type,
            'recipe_id': self.recipe_id,
            'group_id': self.group_id,
        }
