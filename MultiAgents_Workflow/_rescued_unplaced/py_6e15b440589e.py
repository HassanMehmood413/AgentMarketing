from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)

sessionlocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base = declarative_base()
    

async def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
