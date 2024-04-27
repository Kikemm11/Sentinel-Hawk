from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from sqlalchemy.orm import declarative_base



app = Flask(__name__)

Base = declarative_base()

class PaymentMethod(Base):
    __tablename__ = 'payment_method'
    payment_method_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class PaymentMethodConnection:
    conn = None
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
    #Create payment method function 
    
    def write_payment_method(self, data):
        try:
            db_data = PaymentMethod(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Payment method successfully registered'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'Payment method already exists'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Payment method to create payment_method: {str(e)}'}
        finally:
            session.close()
            
    #Read Payment method functions  

    def read_all_payment_methods(self):
        session = self.SessionLocal()
        result = session.query(PaymentMethod).all()
        session.close()
        return result
    
    
    def read_one_payment_method(self, name):
        session = self.SessionLocal()
        result = session.query(PaymentMethod).filter(PaymentMethod.name == name).first()
        session.close()
        return result   

    #Update payment method functions

    def update_payment_method(self, payment_method_id, data): 
        try:
            session = self.SessionLocal()
            payment_method = session.query(PaymentMethod).filter(PaymentMethod.payment_method_id == payment_method_id).first()
            if payment_method:
                payment_method.name = data.get('name')
                session.commit()
                return {'success': True, 'message': 'Payment method successfully updated'}
            else:
                return {'success': False, 'message': 'Cannot find the payment method with the provided id'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to update payment method: {str(e)}'}
        finally:
            session.close()

    #Delete payment method function

    def delete_payment_method(self, payment_method_id): 
        try:
            session = self.SessionLocal()
            payment_method = session.query(PaymentMethod).filter(PaymentMethod.payment_method_id == payment_method_id).first()
            if payment_method:
                session.delete(payment_method)
                session.commit()
                return {'success': True, 'message': 'Payment method successfully deleted'}
            else:
                return {'success': False, 'message': 'Cannot find the payment method with the provided id'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to delete payment method: {str(e)}'}
        finally:
            session.close()
            
    


