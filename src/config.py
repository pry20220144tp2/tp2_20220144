class Config:
    SECRET_KEY = 'asdasd'

class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'tdp_phising'


config={
    'development':DevelopmentConfig
}

