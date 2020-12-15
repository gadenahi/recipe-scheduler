import os
import sys

print('Creating database tables for Family Recipes app...')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    print('os.curdir', os.path.abspath(os.curdir))
    sys.path.append(os.path.abspath(os.curdir))

from recipe_scheduler import db, create_app, bcrypt
from recipe_scheduler.models import User, Group, Role

app = create_app()
ctx = app.app_context()
ctx.push()
db.drop_all()
db.create_all()


# group1 = Group(group_name="default")
# group2 = Group(group_name="group1")
# db.session.add(group1)
# db.session.add(group2)

admin = Role(role_name="admin")
db.session.add(admin)
db.session.commit()

password = 'admin'
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
user = User(
    email="admin@test.com",
    password=hashed_password,
    # current_group=group1.id
)
db.session.add(user)
db.session.commit()
group1 = Group(group_name="default", created_by=user.id)
group2 = Group(group_name="group1", created_by=user.id)
db.session.add(group1)
db.session.add(group2)
db.session.commit()
user.current_group = group1.id
db.session.commit()
user.user_groups.append(group1)
user.user_groups.append(group2)
user.roles.append(admin)
db.session.commit()
