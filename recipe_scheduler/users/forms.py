from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     SelectField, SelectMultipleField, widgets)
from wtforms.validators import (DataRequired, Email, EqualTo, InputRequired,
                                Length, ValidationError)
from recipe_scheduler.models import User


class RegistrationForm(FlaskForm):
    """
    Form for user site
    """
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        """
        To validate the email if it is already exist
        :param email: email on the form
        :return: if email submitted form is already exist, return error
        """
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('The email is used already')


class LoginForm(FlaskForm):
    """
    Form for login site
    """
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class UpdateAccountForm(FlaskForm):
    """
    Form for update account
    """
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Update')

    def validate_email(self, email):
        """
        To validate the email if it is already exist
        :param email: email on the form
        :return: if email submitted form is already exist, return error
        """
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('The email is used already')


class UpdatePasswordForm(FlaskForm):
    """
    Form for update password
    """
    oldpassword = PasswordField(
        'Old Password',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'New Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Update Password')


class GroupForm(FlaskForm):
    """
    Form for update account
    """

    group_name = StringField(
        'Group',
        validators=[DataRequired()]
    )
    submit = SubmitField('Update')


