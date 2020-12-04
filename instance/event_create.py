import os
import sys
import datetime

print('Creating Event database tables for Family Recipes app...')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    print('os.curdir', os.path.abspath(os.curdir))
    sys.path.append(os.path.abspath(os.curdir))


from recipe_scheduler import db, create_app
from recipe_scheduler.models import Recipe, Event
import random


app = create_app()
ctx = app.app_context()
ctx.push()

from recipe_scheduler.main.utils import MonthCalendar

all_recipes = Recipe.query.all()
list_recipes = [i.to_dict() for i in all_recipes]

dt_now = datetime.datetime.now(datetime.timezone(
    datetime.timedelta(hours=-8)))
year, month = dt_now.year, dt_now.month
my_calendar = MonthCalendar()
group = 1
context = my_calendar.get_context_data(year, month, group)


for week in context['month_days']:
    for date in week:
        for type in range(3):
            test_event = Event(
                event_date=date,
                event_type=type,
                recipe_id=random.choice(list_recipes)["id"],
                group_id=1
            )
            db.session.add(test_event)
db.session.commit()
