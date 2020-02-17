import os


class Config:

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DEBUG = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:180052@localhost:3306/xsy'


class DevelopConfig(Config):

    DEBUG = True


class ProductConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'


envs = {
    "dev": DevelopConfig,
    "prod": ProductConfig
}