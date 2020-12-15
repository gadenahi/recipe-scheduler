from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from recipe_scheduler import bcrypt, db
from recipe_scheduler.models import User, Group, Role
from recipe_scheduler.users.forms import (
    LoginForm, RegistrationForm, UpdateAccountForm, UpdatePasswordForm,
    GroupForm)


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    """
    To register the account for new users
    :return: if authenticated, redirect to homepage.
    if registration is submitted, redirect to login page.
    At default, render registration page, title, form
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.
                                                        data).decode('utf-8')
        # group = Group(group_name="default")
        # db.session.add(group)
        guest = Role(role_name="guest")
        db.session.add(guest)
        db.session.commit()
        user = User(
            email=form.email.data,
            password=hashed_password,
            # current_group=group.id
        )
        db.session.add(user)
        db.session.commit()
        group = Group(group_name="default", created_by=user.id)
        db.session.add(group)
        db.session.commit()
        user.current_group = group.id
        db.session.commit()
        user.user_groups.append(group)
        user.roles.append(guest)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    """
    To login
    :return: if authenticated, redirected to homepage
    if login form is submitted, and url contains next, redirect to next page,
    otherwise to homepage
    At default render login.html, title, form
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in !', 'success')
            return redirect(next_page) if next_page else redirect(
                url_for('main.home')
            )
        else:
            flash('Login Unsuccessful')

    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
@login_required
def logout():
    """
    To logout
    :return: redirect to homepage
    """
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    To update the account information
    :return: if the form is submitted, redirect to user.account, else render
    account.html, title, form
    """
    select_group = current_user.get_current_group()
    user_list = current_user.user_groups

    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email

    return render_template('account.html', title='Account', form=form,
                           user_list=user_list, select_group=int(select_group))


@users.route('/account/<string:email>/update_password',
             methods=['GET', 'POST'])
@login_required
def update_password(email):
    """
    To update password with authenticated user
    :param email: current login user
    :return: if form is submitted, redirect to users.account
    At default, render update_password.html, title, form
    """
    select_group = current_user.get_current_group()
    user_list = current_user.user_groups
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.oldpassword.data):
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated', 'success')
            return redirect(url_for('users.account'))

    return render_template('update_password.html',
                           title='Update Password', form=form,
                           user_list=user_list, select_group=int(select_group))


@users.route('/groups', methods=['GET', 'POST'])
@login_required
def show_groups():
    """
    To update the groups
    :return:
    """
    select_group = current_user.get_current_group()
    user_list = current_user.user_groups

    form = GroupForm()

    if form.validate_on_submit():
        check_group = Group.query.filter_by(group_name=form.group_name.data).all()
        check_status = False
        for group in check_group:
            if group in current_user.user_groups:
                check_status = True
                flash('Group name is already exist', 'warning')
        if check_status is False:
            group = Group(
                group_name=form.group_name.data,
                created_by=current_user.id
            )
            current_user.user_groups.append(group)
            db.session.commit()
            flash('The group has been created', 'success')
            return redirect(url_for('users.show_groups'))

    groups = [r.to_dict() for r in current_user.user_groups]

    return render_template('show_groups.html', title='Groups List',
                           groups=groups, user_list=user_list,
                           select_group=int(select_group), form=form)


@users.route('/groups/<int:group_id>', methods=['GET', 'POST'])
@login_required
def update_groups(group_id):
    """
    To update the groups
    :return:
    """
    select_group = current_user.get_current_group()
    user_list = current_user.user_groups
    group = Group.query.filter_by(id=group_id).filter_by(
        created_by=current_user.id).first()
    form = GroupForm()

    if form.validate_on_submit():
        group.group_name = form.group_name.data
        db.session.commit()
        flash('Your group has been updated', 'success')
        return redirect(url_for('users.show_groups'))
    elif request.method == 'GET':
        form.group_name.data = group.group_name

    return render_template('update_groups.html', title='Update Groups',
                           form=form, group_id=group_id,
                           user_list=user_list, select_group=int(select_group))


@users.route('/groups/<int:group_id>/delete', methods=['POST'])
@login_required
def delete_group(group_id):
    """
    To delete the event
    :param group_id: unique number by event
    :return: redirect to homepage
    """
    group = Group.query.get_or_404(group_id)
    # if group in current_user.user_groups:
    if group.created_by == current_user.id:
        current_user.user_groups.remove(group)
        db.session.delete(group)
        db.session.commit()
        flash('Your group has been deleted', 'success')
    else:
        flash('No Authorization')

    return redirect(url_for('users.show_groups'))
