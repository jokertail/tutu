from app.orm import init_orm
from flask_bootstrap import Bootstrap
from app.service import login_manager


def init_ext(app):
    init_orm(app)
    Bootstrap(app)
    login_manager.init_app(app)


