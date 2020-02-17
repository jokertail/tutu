from flask_login import LoginManager

from app.orm.models import User

login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(uid=user_id).first()
    return user


