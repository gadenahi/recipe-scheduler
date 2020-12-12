from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import current_user, login_required
from recipe_scheduler import db
from recipe_scheduler.models import Recipe, Category
from recipe_scheduler.categories.forms import RecipeForm, CategoryForm, URLForm
from recipe_scheduler.categories.utils import parse_html

categories = Blueprint('categories', __name__)


@categories.route('/categories/new_category', methods=['GET', 'POST'])
@login_required
def new_category():
    """
    To post new category
    :return:
    """
    form = CategoryForm()
    select_group = current_user.get_current_group()
    if form.validate_on_submit():
        category = Category(
            category_name=form.category_name.data,
            group_id=select_group
        )
        db.session.add(category)
        db.session.commit()
        flash('The category has been created', 'success')
        return redirect(url_for('categories.new_category'))

    user_list = current_user.user_groups

    return render_template('new_category.html', form=form, user_list=user_list,
                           select_group=int(select_group))


@categories.route('/categories/show', methods=['GET'])
@login_required
def show_categories():
    """
    show list of categories
    :return:
    """
    select_group = current_user.get_current_group()
    all_categories = Category.query.filter_by(group_id=select_group)\
        .order_by(Category.category_name).all()
    categories_list = [c.to_dict() for c in all_categories]
    # categories_list = sorted(categories_list, key=lambda x: x['category_name'])

    user_list = current_user.user_groups
    return render_template('show_categories.html',
                           categories_list=categories_list,
                           user_list=user_list,
                           select_group=int(select_group))


@categories.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    """
    show recipe
    :return:
    """
    category = Category.query.filter_by(id=category_id).first()
    recipe = Recipe.query.filter_by(category_id=category_id).first()

    if recipe:
        flash('Please remove recipe first', 'warning')
        all_recipes = Recipe.query.filter_by(category_id=category_id).all()
        recipes_list = [c.to_dict() for c in all_recipes]
        return render_template('show_recipes.html', recipes_list=recipes_list,
                               category_id=category_id)
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Your category has been deleted', 'success')
        all_categories = Category.query.order_by(Category.category_name).all()
        categories_list = [c.to_dict() for c in all_categories]
        return redirect(url_for('categories.show_categories',
                                categories_list=categories_list
                                ))


@categories.route('/categories/<int:category_id>/recipes', methods=['GET'])
@login_required
def show_recipes(category_id):
    """
    show list of recipes id
    :return:
    """

    category = Category.query.filter_by(id=category_id).first()

    if current_user.current_group != category.group_id:
        flash("Please select the appropriate group", 'error')
        return redirect(url_for('main.home'))

    select_group = current_user.get_current_group()
    user_list = current_user.user_groups
    all_recipes = Recipe.query.filter_by(category_id=category_id).all()
    recipes_list = [c.to_dict() for c in all_recipes]
    return render_template('show_recipes.html', recipes_list=recipes_list,
                           category_id=category_id, user_list=user_list,
                           select_group=int(select_group))


@categories.route('/categories/<int:category_id>/new_recipe', methods=['GET',
                                                                       'POST'])
@login_required
def new_recipe(category_id):
    """
    To post new recipe
    :return:
    """
    url_form = URLForm()
    title, description = None, None
    if url_form.validate_on_submit():
        html = parse_html(url_form.recipe_url.data)
        title = html['title']
        description = html['description']

    category = Category.query.filter_by(id=category_id).first()

    if current_user.current_group != category.group_id:
        flash("Please select the appropriate group", 'error')
        return redirect(url_for('main.home'))

    select_group = current_user.get_current_group()
    user_list = current_user.user_groups
    categories = Category.query.order_by(Category.category_name).all()
    form = RecipeForm()
    form.category_id.choices = [(r.id, r.category_name) for r in categories]
    if form.validate_on_submit():
        recipe = Recipe(
            recipe_name=form.recipe_name.data,
            recipe_url=form.recipe_url.data,
            description=form.description.data,
            category_id=form.category_id.data
        )
        db.session.add(recipe)
        db.session.commit()
        flash('The recipe has been created', 'success')
        return redirect(url_for('categories.new_recipe',
                                category_id=category_id))
    if category_id:
        form.category_id.data = category_id
    if title:
        form.recipe_name.data = title
    if description:
        form.description.data = description
    return render_template('new_recipe.html', form=form, title="New Recipe"
                           , user_list=user_list,
                           select_group=int(select_group), url_form=url_form)


@categories.route('/categories/<int:category_id>/recipes/<int:recipe_id>',
                  methods=['GET', 'POST'])
@login_required
def show_recipe(category_id, recipe_id):
    """
    show recipe
    :return:
    """
    category = Category.query.filter_by(id=category_id).first()

    if current_user.current_group != category.group_id:
        flash("Please select the appropriate group", 'error')
        return redirect(url_for('main.home'))
    select_group = current_user.get_current_group()
    user_list = current_user.user_groups
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    form = RecipeForm()
    categories = Category.query.order_by(Category.category_name).all()
    form.category_id.choices = [(r.id, r.category_name) for r in categories]
    if form.validate_on_submit():
        recipe.recipe_name = form.recipe_name.data
        recipe.recipe_url = form.recipe_url.data
        recipe.description = form.description.data
        recipe.category_id = form.category_id.data
        db.session.commit()
        flash('Your recipe has been updated!', 'success')
        return redirect(url_for('categories.show_recipes',
                                category_id=form.category_id.data))
    elif request.method == 'GET':
        form.recipe_name.data = recipe.recipe_name
        form.recipe_url.data = recipe.recipe_url
        form.description.data = recipe.description
        form.category_id.data = recipe.category_id

    return render_template('new_recipe.html', form=form, title="Update Recipe",
                           recipe_id=recipe_id, category_id=category_id,
                           user_list=user_list, select_group=int(select_group))


@categories.route('/categories/<int:category_id>/recipes/<int:recipe_id>/'
                  'delete', methods=['POST'])
@login_required
def delete_recipe(category_id, recipe_id):
    """
    show recipe
    :return:
    """
    category = Category.query.filter_by(id=category_id).first()

    if current_user.current_group != category.group_id:
        flash("Please select the appropriate group", 'error')
        return redirect(url_for('main.home'))

    recipe = Recipe.query.filter_by(id=recipe_id).first()
    db.session.delete(recipe)
    db.session.commit()
    flash('Your recipe has been deleted', 'success')
    return redirect(url_for('categories.show_recipes',
                            category_id=category_id))
