import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from the .env file (like DATABASE_URL)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# The "engine" is SQLAlchemy's connection manager to the actual database.
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory that creates new database sessions.
# A "session" is like a temporary workspace for talking to the DB
# (reading/writing data) during a single request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class that all our database models (tables) will
# inherit from. SQLAlchemy uses this to know which Python classes
# represent actual database tables.
Base = declarative_base()


# This function provides a database session to API endpoints,
# and makes sure it's properly closed afterward, even if an error occurs.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
