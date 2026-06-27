from app.db.session import engine
from app.db.base import Base
from app.db.models import *  # noqa

def init_db():
    Base.metadata.create_all(bind=engine)


# Creates all tables defined in the models, initializes the whole db schema(all its tables) 