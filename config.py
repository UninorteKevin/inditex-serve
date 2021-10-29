class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:A@localhost/inditex_dba'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
}