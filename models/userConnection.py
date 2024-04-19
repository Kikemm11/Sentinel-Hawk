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
       
    #Read users functions    
       
    def read_one_user(self, username):
        session = self.SessionLocal()
        result = session.query(User).filter(User.username == username).first()
        session.close()
        return result   
    
    def read_all_users(self):
        session = self.SessionLocal()
        result = session.query(User).all()
        session.close()
        return result 
    
    # Create user function
    
    def write_user(self, data):
        try:
            db_data = User(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'User successfully registered'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'User already exists.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to create user: {str(e)}'}
        finally:
            session.close()
    
    #Update user functions

    def update_user(self, vehicle_id, data): 
        try:
            session = self.SessionLocal()
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.username = data.get('username')
                user.password = data.get('password')
                session.commit()
                return {'success': True, 'message': 'User successfully updated'}
            else:
                return {'success': False, 'message': 'Cannot find the user with the provided id'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to update user: {str(e)}'}
        finally:
            session.close()
            
    #Delete user function

    def delete_user(self, user_id): 
        try:
            session = self.SessionLocal()
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
                return {'success': True, 'message': 'User successfully deleted'}
            else:
                return {'success': False, 'message': 'Cannot find the user with the provided id'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to delete user: {str(e)}'}
        finally:
            session.close()