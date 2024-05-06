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
       
    def read_one_vehicle_type(self, name):
        session = self.SessionLocal()
        result = session.query(VehicleType).filter(VehicleType.name == name).first()
        session.close()
        return result    
    
    def write_vehicle_type(self, data):#create
        try:
            db_data = VehicleType(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
            return {'success': True, 'message': 'Tipo de vehículo registrado correctamente.'}
        except IntegrityError:
            session.rollback()
            return {'success': False, 'message': 'El tipo de vehículo ya existe.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al insertar tipo de vehículo: {str(e)}'}
        finally:
            session.close()

    def read_all_vehicle_types(self): #read
        session = self.SessionLocal()
        result = session.query(VehicleType).all()
        session.close()
        return result


    def update_vehicle_type(self, vehicle_id, data): #update
        try:
            session = self.SessionLocal()
            vehicle = session.query(VehicleType).filter(VehicleType.vehicle_type_id == vehicle_id).first()
            if vehicle:
                vehicle.name = data.get('name')
                vehicle.charge = data.get('charge')
                session.commit()
                return {'success': True, 'message': 'Tipo de vehículo actualizado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el tipo de vehículo con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al actualizar tipo de vehículo: {str(e)}'}
        finally:
            session.close()


    def delete_vehicle_type(self, vehicle_id): #delete
        try:
            session = self.SessionLocal()
            vehicle = session.query(VehicleType).filter(VehicleType.vehicle_type_id == vehicle_id).first()
            if vehicle:
                session.delete(vehicle)
                session.commit()
                return {'success': True, 'message': 'Tipo de vehículo eliminado correctamente.'}
            else:
                return {'success': False, 'message': 'No se encontró el tipo de vehículo con el ID proporcionado.'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Error al eliminar tipo de vehículo: {str(e)}'}
        finally:
            session.close()




# Crear una conexión
#connection = VehicleConnection("postgresql://dasl0201:123456@localhost:5432/sentinel_hawk")

# Leer un tipo de vehículo
#tipo_vehiculo = connection.read_one_vehicle_type('Automóvil')

# Escribir un nuevo tipo de vehículo
#resultado = connection.write_vehicle_type({'name': 'Bus', 'charge': 400.25})
#print(resultado)


