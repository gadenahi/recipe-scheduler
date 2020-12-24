import datetime, random
from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from recipe_scheduler import db
from recipe_scheduler.models import Category, Event, Recipe
from recipe_scheduler.main.utils import MonthCalendar
from recipe_scheduler.events.forms import RandomEventForm


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
@main.route('/home/<int:year>/<int:month>', methods=['GET', 'POST'])
@login_required
def home(year=None, month=None):

    select_group = request.form.get('group_options')

    sub_form = RandomEventForm()
    categories = Category.query.filter_by(group_id=current_user.current_group)\
        .order_by(Category.category_name).all()
    sub_form.categories.choices = [(r.id, r.category_name) for r in categories]

    if sub_form.validate_on_submit():
        if not sub_form.event_date.data or not sub_form.event_type.data or \
                not sub_form.categories.data:
            flash('Please select each section on random select', 'warning')
        else:
            all_recipes = Recipe.query.filter(Recipe.category_id.in_(
                sub_form.categories.data)).all()
            list_recipes = [i.to_dict() for i in all_recipes]
            [year, month] = sub_form.event_date.data.split('-')
            my_calendar = MonthCalendar()
            group = current_user.current_group
            context = my_calendar.get_context_data(
                int(year), int(month), group)
            for week in context['month_days']:
                for date in week:
                    if date.year == int(year) and date.month == int(month):
                        for e_type in sub_form.event_type.data:
                            existing_event = Event.query.filter_by(
                                event_date=date).filter_by(
                                event_type=e_type).filter(
                                Event.group_id ==
                                current_user.current_group).first()
                            if not existing_event:
                                event = Event(
                                    event_date=date,
                                    event_type=e_type,
                                    recipe_id=random.choice(list_recipes)["id"],
                                    group_id=group
                                )
                                db.session.add(event)
                            else:
                                existing_event.recipe_id = \
                                    random.choice(list_recipes)["id"]
            db.session.commit()

    if not select_group:
        select_group = current_user.current_group

    if not year and not month:
        dt_now = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(hours=-8)))
        year, month = dt_now.year, dt_now.month
    my_calendar = MonthCalendar()

    context = my_calendar.get_context_data(year, month, select_group)
    user_list = current_user.user_groups

    print(context)
    return render_template('home.html', context=context, user_list=user_list,
                           select_group=int(select_group),
                           group_title="Groups", sub_form=sub_form)


@main.route('/about')
def about():
    """
    Show about
    :return:
    """
    user_list = None
    select_group = -1
    if current_user.is_authenticated:
        select_group = current_user.get_current_group()
        user_list = current_user.user_groups
    return render_template('about.html', user_list=user_list,
                           select_group=int(select_group))
