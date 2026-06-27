from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
# The core connection manager that handles the actual database connections
# Manages a pool of connections (so you don't create a new one for every request)
# Pool_pre_Ping: Before using a connection from the pool, SQLAlchemy "pings" the database to verify it's still alive

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SessionLocal is a factory that creates new database sessions

def get_db():
    db = SessionLocal()    # → Returns a new database session
    try:
        yield db
    finally:
        db.close()





# The Database URL is essentially the address that tells your application exactly where and how to find your database.


# Redis, qdrant and postgre session are information/data stores that the fastapi backend connects to, we have 3 data sources: Postgres for SQL data, Redis client for Cache data and Qdrant client for Vector embeddings data 

# pip install psycopg2-binary   # PostgreSQL client
# pip install redis             # Redis client  
# pip install qdrant-client     # Qdrant client
# These are just communication drivers or libraries that help us talk to or connect with container images.
