from flask import redirect, request, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class MyModelView(ModelView):
    def is_accessible(self):
        # return current_user.is_admin()
        return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('users.login', next=request.url))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        # if current_user.is_authenticated:
        #     return current_user.is_admin()
        return True
    # https://www.youtube.com/watch?v=NYWEf9bZhHQ
