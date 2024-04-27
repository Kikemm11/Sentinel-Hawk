from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, SmallInteger, func
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from sqlalchemy import and_
from sqlalchemy import cast, Date
from sqlalchemy import func, join
from sqlalchemy.orm import aliased
from models.payment_methodConnection import PaymentMethod



app = Flask(__name__)

Base = declarative_base()

class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(Integer, primary_key=True)
    ticket_id = Column(SmallInteger, nullable=False)
    charge = Column(Float, nullable=False)
    currency_id = Column(SmallInteger, nullable=False)
    payment_method_id = Column(SmallInteger, nullable=False)
    exchange_rate = Column(Float, nullable=False)
    local_currency = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True, server_default=func.now())

class PaymentConnection:
    conn = None
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


    #Create payment function 
    
    def write_payment(self, data):
        try:
            db_data = Payment(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Payment successfully registered'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'Payment already exists'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error to create payment: {str(e)}'}
        finally:
            session.close()


    #Read Payment method functions  

    def read_all_payments(self):
        session = self.SessionLocal()
        result = session.query(Payment).all()
        session.close()
        return result
    
    
    def read_one_payment(self, payment_id):
        session = self.SessionLocal()
        result = session.query(Payment).filter(Payment.payment_id == payment_id).first()
        session.close()
        return result
    
    
    def read_today_payments(self):
        session = self.SessionLocal()
        today = date.today()
        result = session.query(Payment).filter(func.date(Payment.created_at) == today).all()
        session.close()
        return result   
    
    
    def read_payments_in_interval(self, start_date, end_date):
        try:
            session = self.SessionLocal()
            
            # Filtrar los pagos dentro del intervalo de fechas
            result = session.query(Payment).filter(
                and_(
                    cast(Payment.created_at, Date) >= cast(start_date, Date),
                    cast(Payment.created_at, Date) <= cast(end_date, Date)
                )
            ).all()

            session.close()
            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'message': f'Error al intentar recuperar pagos en el intervalo: {str(e)}'}
        
        

    #Delete payment method function

    def delete_payment(self, payment_id): 
        try:
            session = self.SessionLocal()
            payment = session.query(Payment).filter(Payment.payment_id == payment_id).first()
            if payment:
                session.delete(payment)
                session.commit()
                return {'success': True, 'message': 'Payment successfully deleted'}
            else:
                return {'success': False, 'message': 'Cannot find the payment with the provided id'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to delete payment: {str(e)}'}
        finally:
            session.close()
            
    
    #Count payment methods function   
            
                
    def count_payments_by_method(self, start_date, end_date):
        try:
            session = self.SessionLocal()

            payment_method_alias = aliased(PaymentMethod)
            query = session.query(
                Payment.payment_method_id,
                payment_method_alias.name,
                func.count()
            ).join(
                payment_method_alias,
                Payment.payment_method_id == payment_method_alias.payment_method_id
            ).filter(
                and_(
                    func.date(Payment.created_at) >= start_date,
                    func.date(Payment.created_at) <= end_date
                )
            ).group_by(
                Payment.payment_method_id,
                payment_method_alias.name
            ).all()

            return query
        except Exception as e:
            return {'success': False, 'message': f'Error trying to count payments by method: {str(e)}'}
        finally:
            session.close()    
        
    
    
        
    