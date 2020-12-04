from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from recipe_scheduler.models import User
from recipe_scheduler import db


sub = Blueprint('sub', __name__)


@sub.route('/sub_menu', methods=['GET'])
@login_required
def sub_menu():
    """
    Sub menu to change the view of recipe and calendar
    :return:
    """
    select_group = request.args.get('selected_group')
    # if current_user.get_current_group() != select_group:
    #     current_user.update_current_group(select_group)

    current_user.update_current_group(select_group)
    db.session.commit()
    # print("sub", select_group)
    # print("sub", current_user)
    # print("sub", current_user.email)
    # print("sub", current_user.current_group)
    # print("sub", current_user.get_current_group())
    return render_template('sub_menu.html')
#