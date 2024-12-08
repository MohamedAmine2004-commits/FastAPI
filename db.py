from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DB_URI = os.path.join(ROOT_PATH, 'db.db')

engine = create_engine(f"sqlite:///{DB_URI}", echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
