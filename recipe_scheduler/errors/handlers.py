"""
This module to handle the custom error message
"""
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """
    To show the custom error message for 404
    :param error: error code
    :return: render 404.html and error code
    """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    """
    To show the custom error message for 404
    :param error: error code
    :return: render 404.html and error code
    """
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    """
    To show the custom error message for 404
    :param error: error code
    :return: render 500.html and error code
    """
    return render_template('errors/500.html'), 500
