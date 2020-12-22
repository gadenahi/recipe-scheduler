import datetime
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import current_user, login_required
from recipe_scheduler import db
from recipe_scheduler.models import Event, Recipe, Category
from recipe_scheduler.events.forms import EventForm


events = Blueprint('events', __name__)


@events.route('/events/new_event', methods=['GET', 'POST'])
@login_required
def new_event():
    """
    To post new category
    :return:
    """
    select_group = current_user.get_current_group()
    user_list = current_user.user_groups
    select_category = request.args.get('category_id', None)
    select_day = request.args.get('day', None)
    select_recipe = request.args.get('recipe_id', None)
    select_event_type = request.args.get('type', None)

    categories = Category.query.filter_by(group_id=current_user.current_group)\
        .order_by(Category.category_name).all()
    form = EventForm()

    form.recipe_id.choices = [(0, "---")]
    for category in categories:
        if category:
            for recipe in category.recipes:
                form.recipe_id.choices.append((recipe.id, recipe.recipe_name))

    form.category_id.choices = [(0, "---")] + \
                               [(r.id, r.category_name) for r in categories]

    if form.validate_on_submit():
        check_event = Event.query.filter(
            Event.event_type == form.event_type.data).filter(
            Event.event_date == form.event_date.data).filter(
            Event.group_id == current_user.current_group).all()

        if form.recipe_id.data == 0 or form.category_id.data == 0:
            flash('Please select valid category or recipe', 'warning')
        elif not check_event:
            if not select_recipe:
                select_recipe = form.recipe_id.data
            event = Event(
                event_date=form.event_date.data,
                event_type=form.event_type.data,
                recipe_id=select_recipe,
                group_id=current_user.current_group
            )
            db.session.add(event)
            db.session.commit()
            flash('The event has been created', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('The recipe on date and type is already exist', 'warning')

    elif request.method == 'GET':
        if select_day:
            year, month, day = select_day.split('-')
            selected_day = datetime.date(
                year=int(year), month=int(month), day=int(day))
            form.event_date.data = selected_day
        if select_event_type:
            form.event_type.data = select_event_type
        if select_category:
            form.category_id.data = select_category
    return render_template('new_event.html', form=form, title="New Event",
                           user_list=user_list, select_group=int(select_group))


@events.route('/events/<int:event_id>/update', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    """
    To update event
    :return:
    """
    event = Event.query.filter_by(id=event_id).first()

    if current_user.current_group != event.group_id:
        flash("Please select the appropriate group", 'error')
        return redirect(url_for('main.home'))

    select_group = current_user.get_current_group()
    user_list = current_user.user_groups
    event = Event.query.filter_by(id=event_id).first()
    form = EventForm()

    recipes = Recipe.query.all()
    categories = Category.query.filter_by(group_id=current_user.current_group)\
        .order_by(Category.category_name).all()
    recipe = Recipe.query.filter_by(id=event.recipe_id).first()
    form.recipe_id.choices = [(0, "---")] + \
                             [(r.id, r.recipe_name) for r in recipes]
    form.category_id.choices = [(0, "---")] + \
                               [(r.id, r.category_name) for r in categories]

    if form.validate_on_submit():
        event.event_date = form.event_date.data
        event.event_type = form.event_type.data
        event.recipe_id = form.recipe_id.data
        db.session.commit()
        flash('The event has been updated', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.event_date.data = event.event_date
        form.event_type.data = str(event.event_type)
        form.category_id.data = recipe.category_id
        form.recipe_id.data = event.recipe_id

    return render_template('new_event.html', form=form, title="Update Event",
                           event_id=event_id, user_list=user_list,
                           select_group=int(select_group))


@events.route('/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    """
    To delete the event
    :param event_id: unique number by event
    :return: redirect to homepage
    """
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Your event has been deleted', 'success')
    return redirect(url_for('main.home'))
