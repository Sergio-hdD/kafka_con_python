# Primer proyecto Kafka con Python

## Correr aplicación
### 1- Kafka: para los pasos 1 y 2, que implican ejecutar comando/s en terminal, previamente se debe acceder hasta la carpeta principal de Kafka
1A- En una terminal levantar el zookeeper con
```bash
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```
1B- En otra terminal levantar el kafka con
```bash
.\bin\windows\kafka-server-start.bat .\config\server.properties
```
### 2- Pyton
2A- Acceder hasta la carpeta que contiene el archivo "app.py" y correrlo con
```bash
python app.py
```
### 3- Usar Postman/Insomnia para puebas de los métodos (por ahora con datos hardcodeados en app.py)
3A- Crear un topic - methods=['GET','POST']
```bash
http://localhost:5000/new_topic
```
3B- Crear una partición para el topic que se crea - methods=['GET','POST']
```bash
http://localhost:5000/new_partition
```
3C- Agregar uno o varios mensajes al topic que se crea - methods=['POST']... por cada ejecución de este método se agrega un mensaje.
```bash
http://localhost:5000/new_message_notification
```
3D- Traer topics - methods=['GET']
```bash
http://localhost:5000/get_notifications
```

