from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

Base = declarative_base()

class Status(Base):
    __tablename__ = 'status'
    status_id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)

class StatusConnection:
    conn = None
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
    #Read Payment method functions  

    def read_all_statuses(self):
        session = self.SessionLocal()
        result = session.query(Status).all()
        session.close()
        return result
    
    
    