from flask import flash, redirect, session, url_for
from flask_login import current_user
from functools import wraps

from recipe_scheduler.models import User, Category, Group


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('_user_id'):
                return redirect(url_for('users.login'))
            user = User.query.filter_by(id=session['_user_id']).first()
            user_role = user.roles[0].rolename
            if user_role != access_level:
                flash(("You do not have permission to access"), 'error')
                return redirect(url_for('main.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator