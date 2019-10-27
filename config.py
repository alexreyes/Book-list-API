import os 

# default config
class BaseConfig(object): 
    DEBUG = False
    SECRET_KEY = "1rV&Q\xcf\x94\xa8\x93\x7f\x96\xdd\xe7o\xd1\xc4\xceB)\xdc\xa6~\x02E"
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig): 
    DEBUG = True

class ProductionConfig(BaseConfig): 
    DEBUG = False