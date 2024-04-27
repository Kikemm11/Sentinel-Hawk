FROM ubuntu:22.04

# Establecer la variable de entorno DEBIAN_FRONTEND
ENV DEBIAN_FRONTEND=noninteractive

# Instalación de dependencias
RUN apt-get update && apt-get install -y \
    postgresql \
    libglib2.0-0 \
    python3 \
    python3-pip \
    net-tools \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copiar el contenido de tu directorio local al contenedor
COPY . .

# Actualizar e instalar Python y herramientas necesarias
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    python3 \
    python3-pip \
    net-tools \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install --upgrade pip 
RUN pip install typing_extensions==4.5.0
RUN pip install Cython==3.0.2 
RUN pip install numpy==1.23.5 
RUN pip install cython-bbox==0.1.3 
RUN pip install -r libs3.txt
RUN pip install -r libs2.txt
RUN pip install -r libs.txt

# Configuración de PostgreSQL
USER postgres

# Iniciar PostgreSQL y crear el usuario y la base de datos
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER sentinel WITH SUPERUSER PASSWORD 'sentinel';" && \
    createdb -O sentinel sentinel_hawk && \
    /etc/init.d/postgresql stop

# Copiar el archivo SQL y ejecutarlo para inicializar la base de datos
COPY sentinel-hawk.sql /docker-entrypoint-initdb.d/

# Cambiar al usuario root para ejecutar el servicio PostgreSQL y la aplicación principal
USER root

# Ejecutar PostgreSQL y la aplicación principal
CMD service postgresql start && python3 app.py
