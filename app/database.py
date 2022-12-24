from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from psycopg2.extras import RealDictCursor
# import psycopg2
# import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         connection = psycopg2.connect("dbname='fastapi' user='postgres' host='localhost' password='bikram2002'",
#         cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("connected")
#         break
#     except Exception as e:
#         print("unable to connect to the database")
#         print(e)
#         time.sleep(5) 