# Primer proyecto Kafka con Python

# Correr aplicación
## 1- Kafka: para los pasos 1A y 1B, que implican ejecutar comando/s en terminal, previamente se debe acceder hasta la carpeta principal de Kafka
1A- En una terminal levantar el zookeeper con
```bash
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```
1B- En otra terminal levantar el kafka con
```bash
.\bin\windows\kafka-server-start.bat .\config\server.properties
```
## 2- Pyton
2A- Acceder hasta la carpeta que contiene el archivo "app.py" y correrlo con
```bash
python app.py
```
## 3- Usar Postman/Insomnia para puebas de los métodos (por ahora con datos hardcodeados en app.py)
### 3A- Prueba de conexión - methods=['GET']
```bash
http://localhost:5000
```
### 3B- Métodos de Auctions 

- Crear un topic - methods=['POST']
```bash
http://localhost:5000/new_topic_auction

Body
{
	"id_product": 31,
	"id_user_creator": 2,
	"amount_base": 5000,
	"end_date": "2022-11-25"
}
```

- Agregar uno o varios mensajes al topic que se crea - methods=['POST']... por cada ejecución de este método se agrega un mensaje.
```bash
http://localhost:5000/add_offer

Body
{
	"id_product": 31,
	"id_offering_user": 6,
	"amount_offered": 6500
}

```

- Traer topics - methods=['GET']
```bash
http://localhost:5000/get_messages_topic_auction

Body
{
	"id_product": 57
}
```

