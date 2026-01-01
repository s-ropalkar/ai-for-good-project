from sqlalchemy import create_engine

def get_mysql_engine():
    engine = create_engine(
        "mysql+pymysql://username:password@localhost:3306/database_name"
    )
    return engine
