
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:KodyBoi21@localhost/library_db'
    DEBUG = True
    
class TestingConfig:
    pass

class ProductionConfig:
    pass