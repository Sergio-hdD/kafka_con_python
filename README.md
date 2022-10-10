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
### 3B- Métodos de Products (Punto 1 del TP)

- Crear un topic por alta de un producto - methods=['POST']
```bash
http://localhost:5000/new_topic_to_product_new

Body
{
	"id_product": 22,
	"old_name": "name_product_1",
	"old_price": 577
}
```

- Agregar (por modificación) uno o varios mensajes al topic que se crea para un producto - methods=['POST']... por cada ejecución de este método se agrega un mensaje.
```bash
http://localhost:5000/add_message_update_product

Body
{
	"id_product": 22,
	"old_name": "name_product_1",
	"new_name": "new_name_product_1",
	"old_price": 577,
	"new_price": 700,
	"edition_date": "2022-10-7"
}
```
- Traer mensajes del topic del producto - methods=['GET']
```bash
http://localhost:5000/get_messages_topic_product

Body
{
	"id_product": 22
}
```

### 3C- Métodos de Auctions (Puntos 2 y 3, del TP)

- Crear un topic por subasta iniciada - methods=['POST']
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

- Agregar uno o varios mensajes al topic de subasta que se crea - methods=['POST']... por cada ejecución de este método se agrega un mensaje.
```bash
http://localhost:5000/add_offer

Body
{
	"id_product": 31,
	"id_offering_user": 6,
	"amount_offered": 6500
}

```

- Traer mensajes del topic de la subasta - methods=['GET']
```bash
http://localhost:5000/get_messages_topic_auction

Body
{
	"id_product": 57
}
```
### 5 - Métodos de Carrito (Puntos 5 del TP)

- Crear un nuevo carrito - methods=['POST']
```bash
http://localhost:5000/new_topic_cart

Body
{
    "id_cart":12,
    "id_buyer":1,
    "id_seller":1,
    "id_product":31,
    "product_name":"Jabon",
    "price":700,
    "amount":5
}
```

- Añadir nuevo mensaje al topico carrito - methods=['POST']
```bash
http://localhost:5000/add_message_cart

Body
{
    "id_cart":12,
    "id_seller":1,
    "id_product":12,
    "product_name":"Jabon",
    "price":700,
    "amount":2
}
```

- Traer todos los mensajes del topico carrito - methods=['GET']
```bash
http://localhost:5000/get_messages_topic_cart

Body
{
    "id_cart":12
}
```