import requests
from flask import Flask, render_template, Response, redirect, request, jsonify, url_for, session, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
import bcrypt
from flask_cors import CORS
import os
from datetime import datetime
import time
import loginApp
from models.vehicle_typeConnection import VehicleConnection
from models.userConnection import UserConnection
from models.currencyConnection import CurrencyConnection
from models.payment_methodConnection import PaymentMethodConnection
from models.ticketConnection import TicketConnection
from models.status2Connection import StatusConnection
from models.paymentConnection import PaymentConnection

"""

import threading  # Importa el módulo threading para detener los procesos en ejecución
from models.deteccion import iniciarDeteccion
from models.statusConnection import DatabaseManager
# Variable global para controlar si el botón está activo o no
button_active = False
# Variable global para almacenar la referencia al hilo de ejecución
execution_thread = None

"""


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
        
"""

#---------------------------- detection funtions -----------------------------

# Código que quieres ejecutar cuando el botón está activo
def execute_code():
    iniciarDeteccion()
    #print("detectando")


# Función para iniciar la ejecución del código en un hilo separado
def start_execution():
    global execution_thread
    execution_thread = threading.Thread(target=execute_code)
    execution_thread.start()

# Función para detener la ejecución del código y limpiar recursos
def stop_execution():
    global execution_thread
    if execution_thread and execution_thread.is_alive():
        # Detener el hilo de ejecución si está en ejecución
        # Aquí debes implementar la lógica para detener cualquier proceso en ejecución
        # Por ejemplo, si tienes un bucle en execute_code, debes salir de ese bucle

        execution_thread.join()  # Esperar a que el hilo termine    


#--------------------------------------------------------------

"""


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
            response, data_from_db = loginApp.get_user(data)
            permisology = data_from_db.permisology
            username = data_from_db.username
            if response == True:
                # Si las credenciales son correctas, inicia sesión con Flask-Login
                user = User(username)
                session['permisology'] = permisology  # Almacena el rol en la sesión
                session['username'] = username
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
#@login_required
def begin():
    permisology = session['permisology']
    username = session['username']
    
    if permisology == "admin":
        return render_template('admin_main.html', username=username)
    else:
        return render_template('employee_main.html', username=username)


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

# Add new vehicle route (No needed)

"""
@app.route('/add-vehicle', methods=['GET', 'POST'])
def add_vehicle_type():

    if 'vehicleName' in request.form and 'vehicleCharge' in request.form:
        name = request.form['vehicleName']
        charge = request.form['vehicleCharge']

        data = {"name": name, "charge": charge}

        connection = VehicleConnection(loginApp.database)
        vehicle_types = connection.write_vehicle_type(data)
        return redirect('/vehicle-type')  
        
"""

# Update vehicle route


@app.route('/update-vehicle', methods=['GET', 'POST'])
def update_vehicle_type():

    if  'newVehicleCharge' in request.form:
        
        charge = request.form['newVehicleCharge']
        vehicle_id = request.form['vehicleId']

        data = {"charge": charge }
        connection = VehicleConnection(loginApp.database)
        vehicle_update = connection.update_vehicle_type(vehicle_id,data)
                
        return redirect('/vehicle-type')       


# Delete vehicle route (No needed)

"""
@app.route('/delete-vehicle/<int:vehicle_id>', methods=['POST'])
def delete_vehicle_type(vehicle_id):
 
    connection = VehicleConnection(loginApp.database)
    resultado = connection.delete_vehicle_type(vehicle_id)
    if resultado['success']:
        return redirect('/vehicle-type')  
        #return resultado['message']
    else:
        return "Error: " + resultado['message']
""" 
    
    
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
    
    
    if 'username1' in request.form and 'password1' in request.form and 'password2' in request.form and 'userPermisology' in request.form:
        
            connection = UserConnection(loginApp.database)
            users = connection.read_all_users()
        
            username = request.form['username1']
            password = request.form['password1']
            password2 = request.form['password2']
            permisology = request.form['userPermisology']
            
            flag = True
            
            if not password or not password2 or not username or not permisology:
                flag = False
            
            if flag == True:
                
                if password == password2:
                    
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    data = {"username": username, "password":  hashed_password, "permisology": permisology }
                    
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

    if 'newUsername' in request.form and 'newUserPassword' in request.form and 'newUserPermisology' in request.form:
        
        username = request.form['newUsername']
        password = bcrypt.hashpw(request.form['newUserPassword'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        permisology = request.form['newUserPermisology']
        user_id = request.form['userId']

        data = {"username": username,"password": password, "permisology": permisology  }
        connection = UserConnection(loginApp.database)
        user_update = connection.update_user(user_id,data)
                
        return redirect('/manage-users')


# Delete user route

@app.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    
    connection = UserConnection(loginApp.database)
    users = connection.read_all_users()
 
    if user_id == 1:
        message = "Sorry, you cannot delete the admin user"
        return render_template('manage_users.html', message=message, tipo='danger', users=users)  
 
    resultado = connection.delete_user(user_id)
    if resultado['success']:
        return redirect('/manage-users')  
    else:
        return "Error: " + resultado['message']
    
    

#---Ticket routes---


# Ticket index route

@app.route('/ticket')
def ticket_index():
    ticket_connection = TicketConnection(loginApp.database)
    vehicle_type_connection = VehicleConnection(loginApp.database)
    status_connection = StatusConnection(loginApp.database)
    payment_method_connection = PaymentMethodConnection(loginApp.database)
    currency_connection = CurrencyConnection(loginApp.database)
    
    all_tickets = ticket_connection.read_all_tickets()
       
    vehicle_types = vehicle_type_connection.read_all_vehicle_types()
    statuses = status_connection.read_all_statuses()
    payment_methods = payment_method_connection.read_all_payment_methods()
    currencies = currency_connection.read_all_currencies()
    
    response = requests.get("https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv")
    data = response.json()
    usd_price = data['monitors']['usd']['price']
    
    return render_template('ticket.html', all_tickets=all_tickets, vehicle_types=vehicle_types, statuses=statuses, payment_methods=payment_methods, currencies=currencies, exchange_rate=usd_price)


# Ticket search route

@app.route('/ticket-search/<string:ticket_id>')
def ticket_search_index(ticket_id):
    
    connection = TicketConnection(loginApp.database)
    vehicle_type_connection = VehicleConnection(loginApp.database)
    status_connection = StatusConnection(loginApp.database)
    payment_method_connection = PaymentMethodConnection(loginApp.database)
    currency_connection = CurrencyConnection(loginApp.database)
    
    ticket = connection.read_one_ticket(ticket_id)
    vehicle_types = vehicle_type_connection.read_all_vehicle_types()
    statuses = status_connection.read_all_statuses()
    payment_methods = payment_method_connection.read_all_payment_methods()
    currencies = currency_connection.read_all_currencies()
    
    response = requests.get("https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv")
    data = response.json()
    usd_price = data['monitors']['usd']['price']
    
    return render_template('ticket_search.html', ticket=ticket, vehicle_types=vehicle_types, statuses=statuses, payment_methods=payment_methods, currencies=currencies, exchange_rate=usd_price)


# Cancel ticket route

@app.route('/cancel-ticket/<int:ticket_id>', methods=['GET', 'POST'])
def cancel_ticket(ticket_id):

    connection = TicketConnection(loginApp.database)
    updated_ticket = connection.update_ticket(ticket_id, 3)
                
    return redirect('/ticket')



# Ticket filter functions

@app.template_filter('get_vehicle_type_name')
def get_vehicle_type_name(vehicle_types, vehicle_type_id):
    for vehicle_type in vehicle_types:
        if vehicle_type.vehicle_type_id == vehicle_type_id:
            return vehicle_type.name
    return None

@app.template_filter('get_status_name')
def get_status_name(statuses, status_id):
    for status in statuses:
        if status.status_id == status_id:
            return status.name
    return None

    
#---Currency routes---



# Currency index route

@app.route('/currency')
def currency_index():
    connection = CurrencyConnection(loginApp.database)
    currencies = connection.read_all_currencies()
    return render_template('currency.html', currencies=currencies)

# Currency search route

@app.route('/currency-search/<string:currency_name>')
def currency_search_index(currency_name):
    connection = CurrencyConnection(loginApp.database)
    currency = connection.read_one_currency(currency_name)
    return render_template('currency_search.html', currency=currency)

# Add new currency route

@app.route('/add-currency', methods=['GET', 'POST'])
def add_currency():

    if 'currencyName' in request.form and 'currencyCode' in request.form:
        name = request.form['currencyName']
        code = request.form['currencyCode']

        data = {"name": name, "code": code}

        connection = CurrencyConnection(loginApp.database)
        currency = connection.write_currency(data)
        return redirect('/currency')  

# Update currency route

@app.route('/update-currency', methods=['GET', 'POST'])
def update_currency():

    if  'newCurrencyName' in request.form and 'newCurrencyCode' in request.form:
        
        name = request.form['newCurrencyName']
        code = request.form['newCurrencyCode']
        currency_id = request.form['currencyId']

        data = {"name": name, "code": code}
        connection = CurrencyConnection(loginApp.database)
        currency_update = connection.update_currency(currency_id,data)
                
        return redirect('/currency')       

# Delete currency route

@app.route('/delete-currency/<int:currency_id>', methods=['POST'])
def delete_currency(currency_id):
 
    connection = CurrencyConnection(loginApp.database)
    resultado = connection.delete_currency(currency_id)
    if resultado['success']:
        return redirect('/currency')  
        #return resultado['message']
    else:
        return "Error: " + resultado['message']  
    
    
    
#---Payment method routes---

# Payment method type index route

@app.route('/payment-method')
def payment_method_index():
    connection = PaymentMethodConnection(loginApp.database)
    payment_methods = connection.read_all_payment_methods()
    return render_template('payment_method.html', payment_methods=payment_methods)

# Payment method search route

@app.route('/payment-method-search/<string:payment_method_name>')
def payment_method_search_index(payment_method_name):
    connection = PaymentMethodConnection(loginApp.database)
    payment_method = connection.read_one_payment_method(payment_method_name)
    return render_template('payment_method_search.html', payment_method=payment_method)

# Add new payment method route

@app.route('/add-payment-method', methods=['GET', 'POST'])
def add_payment_method():

    if 'paymentMethodName' in request.form:
        name = request.form['paymentMethodName']

        data = {"name": name}

        connection = PaymentMethodConnection(loginApp.database)
        payment_method_index = connection.write_payment_method(data)
        return redirect('/payment-method')  

# Update payment method route

@app.route('/update-payment-method', methods=['GET', 'POST'])
def update_payment_method():

    if  'newPaymentMethodName' in request.form:
        
        name = request.form['newPaymentMethodName']
        payment_method_id = request.form['paymentMethodId']

        data = {"name": name}
        connection = PaymentMethodConnection(loginApp.database)
        payment_method_update = connection.update_payment_method(payment_method_id,data)
                
        return redirect('/payment-method')       

# Delete payment method route

@app.route('/delete-payment-method/<int:payment_method_id>', methods=['POST'])
def delete_payment_method(payment_method_id):
 
    connection = PaymentMethodConnection(loginApp.database)
    resultado = connection.delete_payment_method(payment_method_id)
    if resultado['success']:
        return redirect('/payment-method')  
        #return resultado['message']
    else:
        return "Error: " + resultado['message'] 
    


#---Payment routes---

# Add new payment route

@app.route('/ticket-payment', methods=['GET', 'POST'])
def add_ticket_payment():

    if 'paymentMethod' in request.form and 'paymentCurrency' in request.form and 'newTicketStatus' in request.form and 'ticketId' in request.form:
        
        ticket_id = int(request.form['ticketId'])
        charge = float(request.form['paymentCharge'])
        payment_method = int(request.form['paymentMethod'])
        currency = int(request.form['paymentCurrency'])
        status = int(request.form['newTicketStatus'])
        exchange_rate = float(request.form['paymentExchangeRate'])
        local_currency = float(request.form['paymentLocalCurrency'])

        data = {"ticket_id":ticket_id, "charge":charge, "currency_id":currency, "payment_method_id":payment_method, "exchange_rate":exchange_rate, "local_currency": local_currency}
        
        payment_connection = PaymentConnection(loginApp.database) 
        ticket_connection = TicketConnection(loginApp.database)
        
        payment_index = payment_connection.write_payment(data)
        updated_ticket = ticket_connection.update_ticket(ticket_id, status)
        
        return redirect('/ticket')
    
    
# Daily Operations route


@app.route('/daily-operations', methods=['GET'])
def daily_operations():
 
    payment_connection = PaymentConnection(loginApp.database)
    payments = payment_connection.read_today_payments()
    
    ticket_connection = TicketConnection(loginApp.database)
    tickets = ticket_connection.read_today_tickets()
    
    tickets_payment_dict = { 1:0, 2:0, 3:0}
    tickets_vehicle_type_dict = { 1:0, 2:0, 3:0, 4:0}
    payment_usd = 0
    payment_local = 0
    
    for payment in payments:
        payment_usd += payment.charge
        payment_local += payment.local_currency
    
    for ticket in tickets:
        tickets_payment_dict[ticket.status_id] += 1
        tickets_vehicle_type_dict[ticket.vehicle_type_id] += 1
    
    response = requests.get("https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv")
    data = response.json()
    usd_price = data['monitors']['usd']['price']
        
            
    return render_template('daily_operations.html', tickets_payment_dict=tickets_payment_dict, tickets_vehicle_type_dict=tickets_vehicle_type_dict, payment_usd=payment_usd, payment_local=payment_local, usd_price=usd_price)



   
# Revenues route


# @app.route('/revenues', methods=['GET'])
# def reveneus():
 
#     payment_connection = PaymentConnection(loginApp.database)
    
#     result =  payment_connection.read_payments_in_interval(datetime(2024, 4, 26), datetime(2024, 4, 27))
    
#     print(result)
#     if result['success']:
#         payments_in_interval = result['data']
#         for payment in payments_in_interval:
#             print(payment.payment_id, payment.created_at)
#     else:
#         print("Error:", result['message'])
        
            
#     #return render_template('revenues.html', tickets_payment_dict=tickets_payment_dict, tickets_vehicle_type_dict=tickets_vehicle_type_dict, payment_usd=payment_usd, payment_local=payment_local, usd_price=usd_price)
#     return "hola"

@app.route('/revenues', methods=['GET', 'POST'])
def revenues():
    payment_connection = PaymentConnection(loginApp.database)
    response = requests.get("https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv")
    data = response.json()
    usd_price = data['monitors']['usd']['price'] 
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        print("start_date",start_date, type(start_date))
        print("end_date: ",end_date)
        
        # Realizar la consulta utilizando las fechas proporcionadas
        result = payment_connection.read_payments_in_interval(start_date, end_date)
        
        ticket_connection = TicketConnection(loginApp.database)
        tickets_result = ticket_connection.read_ticket_in_interval(start_date, end_date)
        
        payments = result['data']
        tickets = tickets_result['data']
        
        tickets_payment_dict = { 1:0, 2:0, 3:0}
        tickets_vehicle_type_dict = { 1:0, 2:0, 3:0, 4:0}
        payment_usd = 0
        payment_local = 0
        
        for payment in payments:
            payment_usd += payment.charge
            payment_local += payment.local_currency
    
        for ticket in tickets:
            tickets_payment_dict[ticket.status_id] += 1
            tickets_vehicle_type_dict[ticket.vehicle_type_id] += 1
        
        
         
        
        print("payment_usd: ",payment_usd, "tipo: ", type(payment_usd))
        print("payment_local: ",payment_local, "tipo: ", type(payment_local))
        print("usd_price: ",usd_price)
        print("tickets_vehicle_type_dict: ", tickets_vehicle_type_dict) 
            
            
        
        
        if result['success']:

            # Renderizar la tabla de pagos dentro de la misma plantilla
            return jsonify(payment_usd=payment_usd, payment_local=payment_local,tickets_vehicle_type_dict=tickets_vehicle_type_dict, usd_price=usd_price)
        else:
            error_message = result['message']
            return jsonify({'error': error_message})
    else:
        # Si es una solicitud GET, mostrar el formulario de entrada de fechas
        return render_template('revenues.html',usd_price=usd_price)

    
    
"""
  
#---------------------------- deteccion ---------------------------------------------


# Modify button path to start and stop execution
@app.route('/toggle_button', methods=['POST'])
def toggle_button():
    global button_active
    button_active = not button_active
    db_manager = DatabaseManager(loginApp.database)
    
    db_manager.write_status(1, False)
   

    if button_active:
        db_manager.write_status(1, True)
        start_execution()  # Start code execution when button is active
    else:
        db_manager.write_status(1, False)
        stop_execution()   # Stop code execution when button is inactive

    return jsonify({'button_active': button_active})



#-------------------------------------------------------------------------------------    
    

"""

       


if __name__ == "__main__": 
    
    app.run(host="0.0.0.0", port=5000, debug=True)   