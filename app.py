import requests
from flask import Flask, render_template, Response, redirect, request, jsonify, url_for, session, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
import bcrypt
from flask_cors import CORS
import os
import time
import loginApp
from models.vehiculosConecction import VehicleConnection
from loginApp import database

app = Flask(__name__)

#Static folder route

app.static_folder = 'static'  

#Web app secret key (Need to change)

app.secret_key = '123456789' 

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

def generate_token():
    return secrets.token_urlsafe(16)  

# Set the different routes involoved lin the web application


@login_manager.user_loader
def load_user(user_id):
    return User(user_id) 

@login_manager.unauthorized_handler
def unauthorized():
    flash('Debes iniciar sesión para acceder a esta página', 'danger')
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')    

    
# Login route

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            
            data = {"username": username, "password": password}
            response = loginApp.get_user(data)
            if response == True:
                # Si las credenciales son correctas, inicia sesión con Flask-Login
                user = User(username)
                login_user(user)
                flash('Inicio de sesión exitoso', 'success')
                return redirect('/main')
                # Redirige a la vista '/main' pasando 'nombre' como parámetro
            else:
                mensaje = 'Credenciales incorrectas'
                return render_template('login.html', mensaje=mensaje, tipo='danger')
        else:
            mensaje = 'Por favor, ingresa tanto el nombre de usuario como la contraseña'
            return render_template('login.html', mensaje=mensaje, tipo='danger')    
               
    return render_template('login.html')


# Signup route

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        if 'username1' in request.form and 'password1' in request.form and 'password2' in request.form:
            username = request.form['username1']
            password = request.form['password1']
            password2 = request.form['password2']
            print("username: ", username, "password: ", password, "password2: ", password2)
            
            flag = True
            if not password or not password2 or not username:
                flag = False
            
            if flag == True:
                if password == password2:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    data = {"username": username, "password":  hashed_password }
                    
                    response = loginApp.insert_user(data)
                    
                    if response["success"]:
                        mensaje = response["message"]
                        return render_template('login.html', mensaje=mensaje, tipo='success')
                    
                    else:
                        mensaje = response["message"]
                        return render_template('login.html', mensaje=mensaje, tipo='danger')
                else:
                    mensaje = "Las contraseñas no coinciden"
                    return render_template('login.html', mensaje=mensaje, tipo='danger')       
            
            else:
                mensaje = "Debe llenar todos los campos del formulario"
                return render_template('login.html', mensaje=mensaje, tipo='danger')   
            
        
    return render_template('login.html')


# Main route 

@app.route('/main')
@login_required
def begin():
    return render_template('main.html')

# Vehicle type index route

@app.route('/vehicle-type')
def index():
    connection = VehicleConnection(database)
    vehicle_types = connection.read_all_vehicle_types()
    return render_template('vehicle_type.html', vehicle_types=vehicle_types)

# Vehicle type search route

@app.route('/vehicle-search/<string:vehicle_name>')
def search_index(vehicle_name):
    connection = VehicleConnection(database)
    vehicle = connection.read_one_vehicle_type(vehicle_name)
    return render_template('vehicle_search.html', vehicle_type=vehicle)

# Add new vehicle route

@app.route('/add-vehicle', methods=['GET', 'POST'])
def add():

    if 'newVehicleName' in request.form and 'newVehicleCharge' in request.form:
        name = request.form['newVehicleName']
        charge = request.form['newVehicleCharge']

        data = {"name": name, "charge": charge}

        connection = VehicleConnection("postgresql://kikemm11:04122001@localhost:5432/sentinel_hawk")
        vehicle_types = connection.write_vehicle_type(data)
        return redirect('/vehicle-type')  

# Update vehicle route

@app.route('/update-vehicle', methods=['GET', 'POST'])
def update():

    if  'newCharge' in request.form:
        charge = request.form['newCharge']
        vehicle_id = request.form['vehicleId']


        data = {"charge": charge }

        print("data: ",data)

        connection = VehicleConnection(database)
        
        print("data: ",data)

        vehicle_update = connection.update_vehicle_type(vehicle_id,data)
        
        print("data: ",data)
        
        return redirect('/vehicle-type')       

# Delete vehicle route

@app.route('/delete/<int:vehicle_id>', methods=['POST'])
def delete_vehicle(vehicle_id):
 
    connection = VehicleConnection(database)
    resultado = connection.delete_vehicle_type(vehicle_id)
    if resultado['success']:
        return redirect('/vehicle-type')  
        #return resultado['message']
    else:
        return "Error: " + resultado['message']  


if __name__ == "__main__": 
    
    app.run(host="0.0.0.0", port=5000, debug=True)   