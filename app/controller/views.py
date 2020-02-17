from flask import Blueprint, render_template, flash

from app.orm.db import db

bp = Blueprint('bp', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/createDB')
def create_db():
    db.create_all()
    return "create success"


@bp.route('/dropDB')
def drop_db():
    db.drop_all()
    return "drop success"
