from models.userConnection import UserConnection 
import bcrypt
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
#from fastapi.responses import JSONResponse

# Global variable to set the connection to the database

database = "postgresql://dasl0201:123456@localhost:5432/sentinel_hawk"

def get_user(data):
    conn = UserConnection(database) 
    # Obtener los datos del diccionario
    username = data["username"]
    password = data["password"]
   
    data_from_db = conn.read_one_user(username)
        
    if data_from_db and bcrypt.checkpw(password.encode('utf-8'), data_from_db.password.encode('utf-8')):
        
        return True, data_from_db
        # Aquí puedes hacer lo que necesites si la contraseña es válida
    else:
        
        return False, data_from_db
        # Aquí puedes hacer lo que necesites si la contraseña no es válida
        
        
    # if data:
    #     return data.__dict__
    # else:
    #     raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Entrada no encontrado")


def insert_user(data):
    conn = UserConnection(database) 
    response = conn.write_user(data)    
    return response
    

