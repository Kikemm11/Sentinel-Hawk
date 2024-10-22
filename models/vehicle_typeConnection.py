from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

Base = declarative_base()

class VehicleType(Base):
    __tablename__ = 'vehicle_type'
    vehicle_type_id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)
    charge = Column(Float, nullable=False)

class VehicleConnection:
    conn = None
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
       
    #Create vehicle type function 
    
    def write_vehicle_type(self, data):
        try:
            db_data = VehicleType(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Vehicle type successfully registered'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'vehicle type already exists'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to create vehicle type: {str(e)}'}
        finally:
            session.close()
            
    #Read vehicle type functions  

    def read_all_vehicle_types(self):
        session = self.SessionLocal()
        result = session.query(VehicleType).all()
        session.close()
        return result
    
    
    def read_one_vehicle_type(self, name):
        session = self.SessionLocal()
        result = session.query(VehicleType).filter(VehicleType.name == name).first()
        session.close()
        return result   

    #Update vehicle type functions

    def update_vehicle_type(self, vehicle_id, data): 
        try:
            session = self.SessionLocal()
            vehicle_type = session.query(VehicleType).filter(VehicleType.vehicle_type_id == vehicle_id).first()
            if vehicle_type:
                vehicle_type.charge = data.get('charge')
                session.commit()
                return {'success': True, 'message': 'Vehicle type successfully updated'}
            else:
                return {'success': False, 'message': 'Cannot find the vehicle type with the provided id'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to update vehicle type: {str(e)}'}
        finally:
            session.close()

    #Delete vehicle type function

    def delete_vehicle_type(self, vehicle_id): 
        try:
            session = self.SessionLocal()
            vehicle_type = session.query(VehicleType).filter(VehicleType.vehicle_type_id == vehicle_id).first()
            if vehicle_type:
                session.delete(vehicle_type)
                session.commit()
                return {'success': True, 'message': 'Vehicle type successfully deleted'}
            else:
                return {'success': False, 'message': 'Cannot find the vehicle type with the provided id'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error trying to delete vehicle type: {str(e)}'}
        finally:
            session.close()