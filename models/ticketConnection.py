from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, func
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

Base = declarative_base()

class Ticket(Base):
    __tablename__ = 'ticket'

    ticket_id = Column(Integer, primary_key=True)
    vehicle_type_id = Column(Integer, nullable=False)
    charge = Column(Float, nullable=False)
    status_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True, server_default=func.now())

class TicketConnection:
    conn = None
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
     
    # Create ticket function
     
    def write_ticket(self, data):#create
        try:
            db_data = Ticket(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Ticket successfully registered'}
        except IntegrityError as e:
            session.rollback()
            return {'success': False, 'message': e}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to create ticket: {str(e)}'}
        finally:
            session.close()
            
    #Read users functions 

    def read_all_tickets(self): 
        session = self.SessionLocal()
        result = session.query(Ticket).order_by(Ticket.ticket_id.desc()).all()
        session.close()
        return result
    
    def read_one_ticket(self, ticket_id):
        session = self.SessionLocal()
        result = session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
        session.close()
        return result   
    
    def read_paid_tickets(self): 
        session = self.SessionLocal()
        result = session.query(Ticket).filter(Ticket.status_id == 1).order_by(Ticket.ticket_id.desc()).all()
        session.close()
        return result

    
    def read_unpaid_tickets(self): 
        session = self.SessionLocal()
        result = result = session.query(Ticket).filter(Ticket.status_id == 2).order_by(Ticket.ticket_id.desc()).all()
        session.close()
        return result
    
    def read_canceled_tickets(self): 
        session = self.SessionLocal()
        result = result = session.query(Ticket).filter(Ticket.status_id == 3).order_by(Ticket.ticket_id.desc()).all()
        session.close()
        return result

    #Update ticket function

    def update_ticket(self, ticket_id, status):
        try:
            session = self.SessionLocal()
            ticket = session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
            if ticket:
                ticket.status_id = status
                session.commit()
                return {'success': True, 'message': 'ticket type updated successfully.'}
            else:
                return {'success': False, 'message': 'The ticket type was not found with the provided ID.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error updating ticket type: {str(e)}'}
        finally:
            session.close()

    #Delete user function

    def delete_ticket(self, ticket_id):
        try:
            session = self.SessionLocal()
            ticket = session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
            if ticket:
                session.delete(ticket)
                session.commit()
                return {'success': True, 'message': 'Ticket type removed successfully.'}
            else:
                return {'success': False, 'message': 'No se encontró el tipo de vehículo con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'The ticket type was not found with the provided ID.: {str(e)}'}
        finally:
            session.close()





