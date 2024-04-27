from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

Base = declarative_base()

class Ticket(Base):
    __tablename__ = 'ticket'

    ticket_id = Column(Integer, primary_key=True)
    vehicle_type_id = Column(Integer, nullable=False)
    charge = Column(Float, nullable=False)
    status_id = Column(Integer, nullable=False)

class TicketConnection:
    conn = None
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
    def read_one_ticket(self, name):
        session = self.SessionLocal()
        result = session.query(Ticket).filter(Ticket.name == name).first()
        session.close()
        return result    
    
    def write_ticket(self, data):#create
        try:
            db_data = Ticket(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Tipo de vehículo registrado correctamente.'}
        except IntegrityError as e:
            session.rollback()
            return {'success': False, 'message': e}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al insertar tipo de vehículo: {str(e)}'}
        finally:
            session.close()

    def read_all_ticket(self): #read
        session = self.SessionLocal()
        result = session.query(Ticket).all()
        session.close()
        return result


    def update_ticket(self, vehicle_id, data): #update
        try:
            session = self.SessionLocal()
            vehicle = session.query(Ticket).filter(Ticket.vehicle_type_id == vehicle_id).first()
            if vehicle:
                vehicle.name = data.get('name')
                vehicle.charge = data.get('charge')
                session.commit()
                return {'success': True, 'message': 'Vehicle type updated successfully.'}
            else:
                return {'success': False, 'message': 'The vehicle type was not found with the provided ID.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error updating vehicle type: {str(e)}'}
        finally:
            session.close()


    def delete_ticket(self, vehicle_id): #delete
        try:
            session = self.SessionLocal()
            vehicle = session.query(Ticket).filter(Ticket.vehicle_type_id == vehicle_id).first()
            if vehicle:
                session.delete(vehicle)
                session.commit()
                return {'success': True, 'message': 'Vehicle type removed successfully.'}
            else:
                return {'success': False, 'message': 'No se encontró el tipo de vehículo con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'The vehicle type was not found with the provided ID.: {str(e)}'}
        finally:
            session.close()





