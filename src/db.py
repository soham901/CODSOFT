from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean


engine = create_engine('sqlite:///local_sqlite.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
