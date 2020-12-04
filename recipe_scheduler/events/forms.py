from flask_wtf import FlaskForm
from wtforms import (DateField, RadioField, SelectField, SubmitField,
                     SelectMultipleField, StringField, widgets)
from wtforms.validators import DataRequired
from recipe_scheduler.events.widgets import MySelect
from recipe_scheduler.models import Recipe, Category


class EventForm(FlaskForm):
    """
    Form for recipe site
    """
    event_date = DateField(
        'Date',
        validators=[DataRequired()]
    )
    event_type = RadioField(
        'Type',
        choices=[("0", "Breakfast"), ("1", "Lunch"), ("2", "Dinner")],
        default="0"
    )

    category_id = SelectField(
        'Category',
        coerce=int
    )

    recipe_id = SelectField(
        'Recipe',
        coerce=int,
        widget=MySelect()
    )

    submit = SubmitField('Post')

    # def __init__(self, category_id=None):
    #     self.category_id = category_id
    #     self._set_params(self.category_id)
    #
    # def _set_params(self, category_id):
    #     if not category_id:
    #         recipes = Recipe.query.all()
    #     else:
    #         recipes = Recipe.query.filter_by(category_id=category_id).all()
    #     categories = Category.query.all()
    #     self.recipe_id.choices = [(r.id, r.recipe_name) for r in recipes]
    #     self.category_id.choices = [(r.id, r.category_name) for r in categories]


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RandomEventForm(FlaskForm):
    event_date = StringField(
        'Date',
        validators=[DataRequired()]
    )
    event_type = MultiCheckboxField(
        'Types',
        choices=[('0', 'breakfast'), ('1', 'lunch'), ('2', 'dinner')]
    )
    categories = MultiCheckboxField(
        'Categories',
        coerce=int
    )

    submit = SubmitField('Random')
