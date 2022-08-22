class Config:
    SECRET_KEY = 'asdasd'

class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'tp220220144'


config={
    'development':DevelopmentConfig
}

