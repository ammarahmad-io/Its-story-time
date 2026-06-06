from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


url = 'postgresql://postgres:12345@localhost:5432/story_time'
engine = create_engine(url)
session = sessionmaker(bind=engine,autoflush=False,autocommit=False)