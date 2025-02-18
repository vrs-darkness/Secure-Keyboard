from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import Column, Integer, String, create_engine
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
load_dotenv()


SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}" # noqa

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = SessionLocal()
Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True, index=True)
    mobile_id = Column(String, index=True)
    status_code = Column(String, index=True)
    data_size = Column(Integer)


class Device(Base):
    __tablename__ = "device"
    device_id = Column(String, primary_key=True, index=True)
    device_name = Column(String, index=True)
    token = Column(String, index=True)


Base.metadata.create_all(bind=engine)


# Initialize Firebase Admin SDK
cred = credentials.Certificate("path-to-your-service-account.json")
firebase_admin.initialize_app(cred)
