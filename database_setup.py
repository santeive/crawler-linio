from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine("sqlite:///db.sqlite")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
