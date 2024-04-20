from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime,Boolean,  TIMESTAMP
from sqlalchemy import func, case
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class DetectionStatus(Base):
    __tablename__ = 'deteccion_status'

    id = Column(Integer, primary_key=True)
    status = Column(Boolean)

    def __init__(self, id, status):
        self.id = id
        self.status = status
        
class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_table(self):
        Base.metadata.create_all(bind=self.engine)

    def write_status(self, id, status):
        session = self.SessionLocal()
        # Buscar el registro existente con el id proporcionado
        detection_status = session.query(DetectionStatus).filter_by(id=id).first()
        if detection_status:
            # Si el registro existe, actualizar el campo status
            detection_status.status = status
            session.commit()
        else:
            # Si el registro no existe, imprimir un mensaje de error
            print(f"No record found with id {id}")
        session.close()

    def read_status(self):
        session = self.SessionLocal()
        status = session.query(DetectionStatus).order_by(DetectionStatus.id.desc()).first()
        session.close()
        return status.status
