import requests
from flask import Flask, render_template, Response, redirect, request, jsonify, url_for, session, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
import bcrypt
from flask_cors import CORS
import os
import time
import loginApp
from models.vehiculosConnection import VehicleConnection
from models.userConnection import UserConnection
#from loginApp import database

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


#---General routes---


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


# Main route 

@app.route('/main')
@login_required
def begin():
    return render_template('main.html')



#---Vehcile routes---



# Vehicle type index route

@app.route('/vehicle-type')
def vehicle_type_index():
    connection = VehicleConnection(loginApp.database)
    vehicle_types = connection.read_all_vehicle_types()
    return render_template('vehicle_type.html', vehicle_types=vehicle_types)

# Vehicle type search route

@app.route('/vehicle-search/<string:vehicle_name>')
def vehicle_type_search_index(vehicle_name):
    connection = VehicleConnection(loginApp.database)
    vehicle = connection.read_one_vehicle_type(vehicle_name)
    return render_template('vehicle_search.html', vehicle_type=vehicle)

# Add new vehicle route

@app.route('/add-vehicle', methods=['GET', 'POST'])
def add_vehicle_type():

    if 'newVehicleName' in request.form and 'newVehicleCharge' in request.form:
        name = request.form['newVehicleName']
        charge = request.form['newVehicleCharge']

        data = {"name": name, "charge": charge}

        connection = VehicleConnection(loginApp.database)
        vehicle_types = connection.write_vehicle_type(data)
        return redirect('/vehicle-type')  

# Update vehicle route

@app.route('/update-vehicle', methods=['GET', 'POST'])
def update_vehicle_type():

    if  'newCharge' in request.form:
        
        charge = request.form['newCharge']
        vehicle_id = request.form['vehicleId']

        data = {"charge": charge }
        connection = VehicleConnection(loginApp.database)
        vehicle_update = connection.update_vehicle_type(vehicle_id,data)
                
        return redirect('/vehicle-type')       

# Delete vehicle route

@app.route('/delete-vehicle/<int:vehicle_id>', methods=['POST'])
def delete_vehicle_type(vehicle_id):
 
    connection = VehicleConnection(loginApp.database)
    resultado = connection.delete_vehicle_type(vehicle_id)
    if resultado['success']:
        return redirect('/vehicle-type')  
        #return resultado['message']
    else:
        return "Error: " + resultado['message']
    
    
    
#---User routes--- 


# User index route

@app.route('/manage-users')
def users_index():
    connection = UserConnection(loginApp.database)
    users = connection.read_all_users()
    return render_template('manage_users.html', users=users)


# User search route

@app.route('/user-search/<string:username>')
def user_search_index(username):
    connection = UserConnection(loginApp.database)
    user = connection.read_one_user(username)
    return render_template('user_search.html', user=user)


# Add new user route

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    
    

    if 'username1' in request.form and 'password1' in request.form and 'password2' in request.form:
        
            connection = UserConnection(loginApp.database)
            users = connection.read_all_users()
        
            username = request.form['username1']
            password = request.form['password1']
            password2 = request.form['password2']
            
            flag = True
            
            if not password or not password2 or not username:
                flag = False
            
            if flag == True:
                
                if password == password2:
                    
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    data = {"username": username, "password":  hashed_password }
                    
                    response = loginApp.insert_user(data)
                    
                    users = connection.read_all_users()
                    
                    if response["success"]:
                        
                        message = response["message"]
                        return render_template('manage_users.html', message=message, tipo='danger', users=users) 
                    
                    else:
                        message = response["message"]
                        return render_template('manage_users.html', message=message, tipo='danger', users=users) 
                else:
                    message = "Passwords are not the same"
                    return render_template('manage_users.html', message=message, tipo='danger', users=users)
            else:
                message = "You must fill all the fields in the form"
                return render_template('manage_users.html', message=message, tipo='danger', users=users) 
            
    return render_template('manage_users.html', message=message, tipo='danger', users=users)   
    
    
# Update user route

@app.route('/update-user', methods=['GET', 'POST'])
def update_user():

    if 'newUsername' in request.form and 'newUserPassword' in request.form:
        
        username = request.form['newUsername']
        password = request.form['newUserPassword']
        user_id = request.form['userId']

        data = {"username": username,"password": password  }
        connection = UserConnection(loginApp.database)
        user_update = connection.update_user(user_id,data)
                
        return redirect('/manage-users')


# Delete user route

@app.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
 
    connection = UserConnection(loginApp.database)
    resultado = connection.delete_user(user_id)
    if resultado['success']:
        return redirect('/manage-users')  
        #return resultado['message']
    else:
        return "Error: " + resultado['message']    


if __name__ == "__main__": 
    
    app.run(host="0.0.0.0", port=5000, debug=True)   