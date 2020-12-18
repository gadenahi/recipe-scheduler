"""
This module is to invite others via email
"""
from flask import url_for
from flask_login import current_user
from flask_mail import Message
from recipe_scheduler import mail


def send_invite_email(email, group):
    """
    To send the email
    :param group: invite by group
    :return: None
    """
    token = group.get_reset_token()
    msg = Message('Invitation to join the group in Recipe Scheduler',
                  recipients=[email])
    msg.body = f'''You are invited this group by {current_user.email}, 
    visit the following
    link: {url_for('users.reset_token', token=token, email=email,
                   _external=True)}
    if you did not request then simply ignore this email or ask the sender
    '''
    msg.html = (f'''<h1>You are invited join the group by {current_user.email} 
                at Food Recipe Scheduler</h1>
                <p>Please visit the following link</p>
                link: {url_for('users.reset_token', token=token,
                               email=email,_external=True)}
                <p>If you did not request then simply ignore
                 this email or ask the sender</p>
    ''')
    mail.send(msg)
