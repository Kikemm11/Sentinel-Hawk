from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

Base = declarative_base()

class Currency(Base):
    __tablename__ = 'currency'
    currency_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String(10), nullable=False)

class CurrencyConnection:
    conn = None
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
    #Create currency function 
    
    def write_currency(self, data):
        try:
            db_data = Currency(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Currency successfully registered'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'Currency already exists'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to create Currency: {str(e)}'}
        finally:
            session.close()
            
    #Read Currency functions  

    def read_all_currencies(self):
        session = self.SessionLocal()
        result = session.query(Currency).all()
        session.close()
        return result
    
    
    def read_one_currency(self, name):
        session = self.SessionLocal()
        result = session.query(Currency).filter(Currency.name == name).first()
        session.close()
        return result   

    #Update Currency functions

    def update_currency(self, currency_id, data): 
        try:
            session = self.SessionLocal()
            currency = session.query(Currency).filter(Currency.currency_id == currency_id).first()
            if currency:
                currency.name = data.get('name')
                currency.code = data.get('code')
                session.commit()
                return {'success': True, 'message': 'Currency successfully updated'}
            else:
                return {'success': False, 'message': 'Cannot find the Currency with the provided id'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to update Currency: {str(e)}'}
        finally:
            session.close()

    #Delete Currency function

    def delete_currency(self, currency_id): 
        try:
            session = self.SessionLocal()
            currency = session.query(Currency).filter(Currency.currency_id == currency_id).first()
            if currency:
                session.delete(currency)
                session.commit()
                return {'success': True, 'message': 'Currency successfully deleted'}
            else:
                return {'success': False, 'message': 'Cannot find the Currency with the provided id'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to delete Currency: {str(e)}'}
        finally:
            session.close()