from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField)
from wtforms.validators import DataRequired


class RecipeForm(FlaskForm):
    """
    Form for recipe site
    """
    recipe_name = StringField(
        'Recipe Name',
        validators=[DataRequired()],
        render_kw={"placeholder": "Recipe Name"}
    )
    recipe_url = StringField(
        'Recipe URL',
        validators=[DataRequired()],
        render_kw={"placeholder": "http://****"}
    )
    description = StringField(
        'Description',
        validators=[DataRequired()],
        render_kw={"placeholder": "Description"}
    )
    category_id = SelectField(
        'Category',
        coerce=int
    )

    submit = SubmitField('Post')


class CategoryForm(FlaskForm):
    """
    Form for Category
    """
    category_name = StringField(
        'Category Name',
        validators=[DataRequired()],
        render_kw={"placeholder": "Category Name"}
    )

    submit = SubmitField('Post')


class URLForm(FlaskForm):
    """
    Form for URL
    """
    recipe_url = StringField(
        'Recipe URL',
        validators=[DataRequired()],
        render_kw={"placeholder": "http://****"}
    )

    submit = SubmitField('GET')
