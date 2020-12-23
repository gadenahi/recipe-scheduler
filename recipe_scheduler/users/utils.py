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
    msg.body = f'''You are invited to join the group by {current_user.email}, 
    at Food Recipe Scheduler
    Food Recipe Scheduler: {url_for('main.home', _external=True)}
    Please visit the following link to join
    link: {url_for('users.reset_token', token=token, email=email,
                   _external=True)}
    if you did not request then simply ignore this email or ask the sender
    ####
    Food Recipe Scheduler
    ####
    '''
    msg.html = (f'''<h4>You are invited to join the group by {current_user.email} 
                at Food Recipe Scheduler</h4>
                Food Recipe Scheduler: {url_for('main.home',_external=True)}
                <p>Please visit the following link to join</p>
                link: {url_for('users.reset_token', token=token,
                               email=email,_external=True)}
                <p>If you did not request then simply ignore
                 this email or ask the sender</p>
                <p>####<br/>
                Food Recipe Scheduler<br/>
                ####
                </p> 
    ''')
    mail.send(msg)
