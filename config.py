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
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'dikwon79@gmail.com'
    MAIL_PASSWORD = 'slfb botv ksyz rltc'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    @staticmethod
    def init_app(app):
        pass
    
    
class DevelopmentConfig(Config):
    DEBUG = True
    # MySQL을 사용하려면 'mysql+pymysql'을 사용합니다.
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dongil:AVNS_yWTxLGovb-KZxZOYHf5@db-mysql-nyc3-87675-do-user-16279834-0.c.db.ondigitalocean.com:25060/dbcomp4537'
                                    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dongil:AVNS_yWTxLGovb-KZxZOYHf5@db-mysql-nyc3-87675-do-user-16279834-0.c.db.ondigitalocean.com:25060/dbcomp4537'
    
class ProductionConfig(Config):
    # MySQL을 사용하려면 'mysql+pymysql'을 사용합니다.
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dongil:AVNS_yWTxLGovb-KZxZOYHf5@db-mysql-nyc3-87675-do-user-16279834-0.c.db.ondigitalocean.com:25060/dbcomp4537'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}