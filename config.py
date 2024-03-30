import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MYAPP_ADMIN = os.environ.get('MYAPP_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    MYAPP_POSTS_PER_PAGE = 10
    MYAPP_COMMENTS_PER_PAGE = 10
    MYAPP_FOLLOWERS_PER_PAGE = 20
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # MySQL을 사용하려면 'mysql+pymysql'을 사용합니다.
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://doadmin:AVNS_gJeBLp6MVV_PyMx3baQ@db-mysql-nyc3-61584-do-user-15802968-0.c.db.ondigitalocean.com:25060/comp4537'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://doadmin:AVNS_gJeBLp6MVV_PyMx3baQ@db-mysql-nyc3-61584-do-user-15802968-0.c.db.ondigitalocean.com:25060/comp4537'

class ProductionConfig(Config):
    # MySQL을 사용하려면 'mysql+pymysql'을 사용합니다.
     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://doadmin:AVNS_gJeBLp6MVV_PyMx3baQ@db-mysql-nyc3-61584-do-user-15802968-0.c.db.ondigitalocean.com:25060/comp4537'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}