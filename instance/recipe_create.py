import os
import sys


print('Creating Category and Recipe database tables for Family Recipes app...')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    print('os.curdir', os.path.abspath(os.curdir))
    sys.path.append(os.path.abspath(os.curdir))


from recipe_scheduler import db, create_app
from recipe_scheduler.models import Recipe, Category
import pandas as pd


app = create_app()
ctx = app.app_context()
ctx.push()

categories = pd.read_excel('instance/categories_format.xlsx')
recipes = pd.read_excel('instance/recipes_format.xlsx')

for index, category in categories.iterrows():
    test_cat = Category(
        category_name=category['category_name'],
        group_id=1
    )
    db.session.add(test_cat)
db.session.commit()

for index, recipe in recipes.iterrows():
    test_cat = Recipe(
        recipe_name=recipe['recipe_name'],
        recipe_url=recipe['recipe_url'],
        description=recipe['description'],
        category_id=recipe['category_id']
    )
    db.session.add(test_cat)
db.session.commit()
