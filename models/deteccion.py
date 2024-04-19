
#************************************************************************************
from os import name
import sys
sys.path.append("/home/dasl/sentinel_last_2/sentinel_hawk/models/detection/ByteTrack")
from yolox.tracker.byte_tracker import BYTETracker, STrack
from onemetric.cv.utils.iou import box_iou_batch
from dataclasses import dataclass
sys.path.append('models/supervision')
import supervision as sv
from supervision.utils.video import VideoInfo,get_video_frames_generator
from supervision.detection.annotate import Detections, BoxAnnotator
from supervision.detection.line_counter import LineZone, LineZoneAnnotator
from supervision.geometry.core import Point
from ultralytics import YOLO
import numpy as np
from tqdm.notebook import tqdm
import cv2
from typing import List
import datetime
import pandas as pd
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
import time
from PIL import Image

from models.vehicle_typeConnection import VehicleConnection 
from models.ticketConection import TicketConnection
from models.statusConecction import  DatabaseManager

# from vehicle_typeConnection import VehicleConnection 
# from ticketConection import TicketConnection
# from statusConecction import  DatabaseManager

Base = declarative_base()

class Deteccion(Base):
    __tablename__ = 'deteccion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    #tipo = Column(String)
    tipo_vehiculo = Column(String)
    hora = Column(String)
    fecha = Column(String)

    
   
class Vehiculo:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.conn = self.engine.connect()

    def write_detection(self, data):
        try:
            db_data = Deteccion(**data)
            session = self.SessionLocal()
            session.add(db_data)
            session.commit()
        except Exception as e:
            print(f"Error al escribir en la base de datos: {e}")
            session.rollback()
        finally:
            session.close()

    def close(self):
        if self.conn:
            self.conn.close()
            
#------------------------------------- prueba ---------------------------- 



#---------------------------------------------------------------------------------------------------------------------

def exportPostgres(tipo):
    conn = None
    database = "postgresql://dasl0201:123456@localhost:5432/sentinel_hawk"
    
    connection = VehicleConnection(database)

    vehicle_update = connection.read_one_vehicle_type(tipo)

    # charge = vehicle_update.charge
    print(vehicle_update.charge)
    
    try:
        conn = Vehiculo(database)
                # Obtener la hora actual
        hora_actual = datetime.datetime.now().time()

        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now().date()

        # Crear un timedelta de 4 horas
        delta_horas = datetime.timedelta(hours=4)

        # Restar 4 horas al tiempo actual
        hora_ajustada = (datetime.datetime.combine(fecha_actual, hora_actual) - delta_horas).time()

        # Verificar si la hora ajustada cruza a la fecha anterior
        if hora_ajustada.hour < hora_actual.hour:
            fecha_ajustada = fecha_actual - datetime.timedelta(days=1)
        else:
            fecha_ajustada = fecha_actual

        # Convertir la hora ajustada a una cadena en el formato deseado
        hora_actual_str = hora_ajustada.strftime("%H:%M:%S")
        fecha = fecha_ajustada.strftime("%Y-%m-%d")


        #hora_actual = datetime.datetime.now().time()
        #hora_actual_str = hora_actual.strftime("%H:%M:%S")
        #fecha = datetime.datetime.now().date().strftime("%Y-%m-%d")

        data = {
            #"tipo": str(line_counter),
            "vehicle_type_id": vehicle_update.vehicle_type_id,
            "charge": vehicle_update.charge,
            "status_id": 1
            
        }
        
        connection = TicketConnection(database)
        vehicle_update = connection.write_ticket(data)
        print(vehicle_update)

        

    except Exception as e:
        print(f"Error en exportPostgres: {e}")

    finally:
        if conn:
            conn.close()





#******************************** programa linea ****************************************

@dataclass(frozen=True)
class BYTETrackerArgs:
    track_thresh: float = 0.25
    track_buffer: int = 30
    match_thresh: float = 0.8
    aspect_ratio_thresh: float = 3.0
    min_box_area: float = 1.0
    mot20: bool = False

# converts Detections into format that can be consumed by match_detections_with_tracks function
def detections2boxes(detections: Detections) -> np.ndarray:
    return np.hstack((
        detections.xyxy,
        detections.confidence[:, np.newaxis]
    ))


# converts List[STrack] into format that can be consumed by match_detections_with_tracks function
def tracks2boxes(tracks: List[STrack]) -> np.ndarray:
    return np.array([
        track.tlbr
        for track
        in tracks
    ], dtype=float)


# matches our bounding boxes with predictions
def match_detections_with_tracks(
    detections: Detections,
    tracks: List[STrack]
) -> Detections:
    if not np.any(detections.xyxy) or len(tracks) == 0:
        return np.empty((0,))

    tracks_boxes = tracks2boxes(tracks=tracks)
    iou = box_iou_batch(tracks_boxes, detections.xyxy)
    track2detection = np.argmax(iou, axis=1)

    tracker_ids = [None] * len(detections)

    for tracker_index, detection_index in enumerate(track2detection):
        if iou[tracker_index, detection_index] != 0:
            tracker_ids[detection_index] = tracks[tracker_index].track_id

    return tracker_ids


# Carga el modelo        
def prepararModelo():        
    # settings
    MODEL = "/home/dasl/sentinel_last_2/sentinel_hawk/models/detection/yolov8n.pt"
    
    model = YOLO(MODEL)
    model.fuse()
    return model    



def iniciarDeteccion():
   
    model = prepararModelo() # Prepara el modelo
    
    
    #coordenadas,lineas_global = leer_coordenadas2(API_URL2)
    
    coordenadas = [((1700, 21),(1700, 2136))]
    lineas_global = ["in"]
    
    # Obtine cada linea
    for linea in coordenadas:
        p1, p2 = linea
        x = p1[0]
        y = p1[1]
        xx = p2[0]
        yy = p2[1]
    
    #obtener la camara
    # res = requests.get(f"{API_URL1}/api/getUrl")
    # cam = res.json()
    # urlCam = str(cam["cam"]) 
    urlCam = "rtsp://admin:placa123@192.168.60.4:554/snl/live/1/1"    
    path = urlCam # URL camara
    capture = cv2.VideoCapture("/home/dasl/sentinel_last_2/sentinel_hawk/models/detection/04.40.00-04.50.00[M][0@0][0].mp4") # URL camara
    
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)) # Obtiene el ancho de la camara
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Obtiene el alto de la camara
    
    byte_tracker = BYTETracker(BYTETrackerArgs())

    
    puntos = []
    i = 0

    for linea in coordenadas: #obtiene los puntos de las lineas y los agrega en la lista puntos
        punto = []
        p1, p2 = linea
        x = p1[0]
        y = p1[1]
        xx = p2[0]
        yy = p2[1]
        puntoI = Point(x, y)
        puntoE = Point(xx, yy)
        punto.append(puntoI)
        punto.append(puntoE)    
        puntos.append(punto)
    
    nombres = [] 
    Lines_counters = []
    Lines_annotators = []
   
    for punto in puntos:       # Crea los puntos de inicio y fin de cada linea    
        LINE_START = punto[0]
        LINE_END = punto[1]
        
        line = LineZone(LINE_START, LINE_END)
        Lines_counters.append(line)
    
    for el in lineas_global:        # Le asigana que sentido tendra cada linea
        n = []
        if str(el) == "in":
            parametro1 = "entrada"
            parametro2 = "salida"
        if str(el) == "out":
            parametro1 = "salida"
            parametro2 = "entrada"

        Lines_annotators.append(LineZoneAnnotator(thickness=4, text_thickness=4, text_scale=2,custom_in_text=parametro1, custom_out_text=parametro2))
        n.append(parametro1)
        n.append(parametro2)
        nombres.append(n)
    
  
    print("detectando")
    i= 0
    box_annotator = BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)
    
    database = "postgresql://dasl0201:123456@localhost:5432/sentinel_hawk"
    db_manager = DatabaseManager(database)
    
    while True:    
        try:
            
            last_status = db_manager.read_status()
            
            if last_status == False:
                capture.release()
                cv2.destroyAllWindows() 
                break
            
            t1 = time.time()
            #
            # if cap_cleaner.last_frame is not None:
            ret, frame = capture.read()

            if not ret:
                print("Error al leer el frame.")
                capture.release()
                cv2.destroyAllWindows() 
                sys.exit()
                break  
            

            results = model(frame, verbose=False)[0]
    
            detections = sv.Detections.from_ultralytics(results)
            names = results.names
            #print(names)

            detections = detections[
                (detections.class_id == 1)|
                (detections.class_id == 2)|
                #(detections.class_id == 3)|
                (detections.class_id == 5)|
                (detections.class_id == 7) 
            ]

            tracks = byte_tracker.update(
                output_results=detections2boxes(detections=detections),
                img_info=frame.shape,
                img_size=frame.shape
            )

            tracker_id = match_detections_with_tracks(detections=detections, tracks=tracks)
            detections.tracker_id = np.array(tracker_id)
            
            labels = [
                f"#{tracker_id} {model.model.names[class_id]}: {confidence:.2f}"
                for _, _, confidence, class_id, tracker_id in detections
            ]


            for i, linea in enumerate(Lines_counters):
                deteccion = linea.trigger(detections)

                if isinstance(deteccion, list):
                    type_detection = names[deteccion[1]] # tipo de deteccion
                    if deteccion[0] == 1:#entrada
                        print("datos :", nombres[i][0], deteccion[0])
                        output_directory = "frames/"

                        exportPostgres(type_detection)
                    elif deteccion[0] == 2:
                        print("datos :", nombres[i][1], deteccion[0])
                        output_directory = "frames/"
                        #exportPostgres("salida", f"linea{i}", API_URL2, type_detection)
                else:
                    pass

            for linea, line_annotator in zip(Lines_counters, Lines_annotators):
                frame = line_annotator.annotate(frame, linea)


            frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
            dsize = (1200,800)
            frameM =cv2.resize(frame,dsize) 
            
                
            
            # cv2.imshow("Camara", frameM)
                
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()
            #     break
            # if cv2.getWindowProperty("Camara", cv2.WND_PROP_VISIBLE) < 1:
            #     break  
        

        except IndexError:

            continue
        
        except Exception as e:
            print(f"Error en el bucle principal: {e}")

            capture.release()
            cv2.destroyAllWindows()
        
    capture.release()
    cv2.destroyAllWindows() 
    sys.exit()
    
            

# if __name__ == "__main__": 
    
#     iniciarDeteccion()
    
