from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from the nearest .env file so the DB URL is available during app startup
load_dotenv(find_dotenv())

DATABASE_URL="postgresql://Cyclova_owner:npg_5NgAcpLuvYb0@ep-red-grass-a4jcxm9u-pooler.us-east-1.aws.neon.tech/Cyclova?sslmode=require&channel_binding=require"

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)

sessionlocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


async def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
