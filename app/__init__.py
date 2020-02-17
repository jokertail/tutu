from flask import Flask

from app.controller import bp, init_view
from app.ext import init_ext
from app.setting import envs


def create_app():
    app = Flask(__name__)

    app.config.from_object(envs.get("dev"))

    app.config['SECRET_KEY'] = '123456'

    init_view(app)

    init_ext(app)

    return app
