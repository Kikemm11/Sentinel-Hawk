from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime,Boolean,  TIMESTAMP
from sqlalchemy import func, case
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError



Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    password = Column(String)


class UserConnection:
    conn = None
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
    def read_one_user(self, username):
        session = self.SessionLocal()
        result = session.query(User).filter(User.username == username).first()
        session.close()
        return result    
    
    
    def write_user(self, data):
        try:
            db_data = User(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Usuario registrado correctamente.'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'El usuario ya existe.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al insertar usuario: {str(e)}'}
        finally:
            session.close()