import pandas as pd
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import current_user, login_required
from recipe_scheduler import db
from recipe_scheduler.models import Recipe, Category, Group


uploads = Blueprint('uploads', __name__)


@uploads.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_recipe():
    """
    To upload the list of recipes
    :return:
    """
    select_group = current_user.get_current_group()
    user_list = current_user.user_groups

    if request.method == 'POST':
        f = request.files['send_file']
        data_xls = pd.read_excel(f)
        for index, data in data_xls.iterrows():
            if data.isnull().any():
                flash('Blank is not allowed, please review the uploaded list',
                      'warning')
                return redirect(url_for('uploads.upload_recipe'))

            user_attr = current_user.to_dict()

            def check_group():
                for group_list in user_attr['user_groups']:
                    if group_list['group_name'] == data['group_name']:
                        return group_list['id']

                return None
            group_id = check_group()

            if not group_id:
                group = Group(group_name=data['group_name'])
                current_user.user_groups.append(group)
                db.session.commit()
                group_id = group.id

            category = Category.query.filter_by(group_id=group_id).\
                filter_by(category_name=data['category_name']).first()

            if not category:
                category = Category(
                    category_name=data['category_name'],
                    group_id=group_id
                )
                db.session.add(category)
                db.session.commit()
            recipe = Recipe(
                recipe_name=data['recipe_name'],
                recipe_url=data['recipe_url'],
                description=data['description'],
                category_id=category.id,
            )
            db.session.add(recipe)

        db.session.commit()
        flash('Your list has been uploaded', 'success')
        return redirect(url_for('main.home'))

    excelformat = url_for(
        'static', filename='recipe_format/' + "recipe_format.xlsx")
    return render_template('upload_recipe.html', title='Upload Recipes',
                           excelformat=excelformat,
                           user_list=user_list, select_group=int(select_group))