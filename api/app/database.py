import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Load environment variables from .env
load_dotenv()

# Read database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set. Add it to your .env file.")


# SQLAlchemy engine manages the database connection
engine = create_engine(DATABASE_URL)


# SessionLocal creates database sessions for queries/inserts
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Create one database session per API request.
    The session is closed after the request finishes.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()