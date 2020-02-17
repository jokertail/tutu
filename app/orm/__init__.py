from . import models
from .db import db


def init_orm(app):
    db.init_app(app)
