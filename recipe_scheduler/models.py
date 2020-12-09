"""
Model
"""
from datetime import datetime
from flask_login import UserMixin
from recipe_scheduler import db, login_manager
from sqlalchemy.orm import relationship, backref


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


class User(db.Model, UserMixin):
    """
    User models for user information
    """
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # groups = db.relationship('Group', secondary='user_groups',
    #                         backref=db.backref('by_groups', lazy='dynamic'))
    # groups = db.relationship('Group', secondary='user_groups')
    user_groups = db.relationship('Group', secondary='user_groups',
                                  backref=db.backref('users', lazy='dynamic'))

    current_group = db.Column(db.Integer, nullable=False)

    def __init__(self, email=None, password=None, current_group=None):
        self.email = email
        self.password = password
        self.current_group = current_group

    # def __init__(self, current_group=None, **kwargs):
    #     super(User, self).__init__(**kwargs)

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


class Group(db.Model):
    """
    Group model
    """
    __table_name__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), unique=False)
    # users = db.relationship('User', backref='user_group', lazy=True)
    # users = db.relationship('User', secondary='user_groups',
    #                         backref=db.backref('by_users', lazy='dynamic'))
    # users = db.relationship('User', secondary='user_groups')
    events = db.relationship('Event', backref='event_group', lazy=True)
    categories = db.relationship('Category', backref='category_group', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
            # 'users': self.users,
            'events': self.events
        }


# class UserGroups(db.Model):
#     """
#     User - Group Model
#     """
#     __table_name__ = 'user_groups'
#
#     id = db.Column(db.Integer, primary_key=True)
#     # user_id = db.Column(db.Integer(),
#     #                     db.ForeignKey('user.id', ondelete='CASCADE'))
#     # group_id = db.Column(db.Integer(),
#     #                     db.ForeignKey('group.id', ondelete='CASCADE'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
#     user = relationship(User, backref=backref("user_groups",
#                                               cascade="all, delete"))
#     group = relationship(Group, backref=backref("user_groups",
#                                                 cascade="all, delete"))
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'group_id': self.group_id
#         }


class Recipe(db.Model):
    """
    Recipe Model
    """
    __table_name__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100), unique=False, nullable=False)
    recipe_url = db.Column(db.String(2083), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    events = db.relationship('Event', backref='recipe', lazy=True, cascade="all")

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
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'event_date': self.event_date,
            'event_type': self.event_type,
            'recipe_id': self.recipe_id,
            'group_id': self.group_id,
        }
