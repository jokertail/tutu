from .views import bp
from .test import test_bp
from .userview import user_bp


def init_view(app):
    app.register_blueprint(bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(user_bp)
