from flask import Flask, render_template, request, g, redirect, url_for
from flask_cors import CORS

# Para la creacion del topic 
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient, NewTopic
import json

app = Flask(__name__)
CORS(app)

admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id="prueba", api_version=(0, 10, 1))
username = 'username_5'


@app.route('/', methods=['GET'])
def hello():
    return "Service (OK)"

@app.route('/new_topic', methods=['GET','POST'])
def create_topic():
	# Creacion del topic para notificaciones (Donde escriben los likes y seguidores nuevos)
	tl2 = []
	topic_notif = username + '_notificaciones'
	tl2.append(NewTopic(name=topic_notif, num_partitions=1, replication_factor=1))
	admin_client.create_topics(new_topics=tl2, validate_only=False)

	return 'new_topic'


@app.route('/new_partition' , methods=['GET','POST'])
def create_partition():
	username = 'Sergio'
	# Creacion de la particion dentro del topic/usuario
	producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)
	producer.send(username, 1)
	producer.close()

	return 'new_partition'

@app.route('/new_message_notification', methods=['POST'])
def create_notification():
	nombre = 'name_current_user'
	titulo = '_title_publicacion'
	autor = username # Nombre del usuario que creo el post
	topic_notif = autor + '_notificaciones'	# Topic del autor donde notifica

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)
	producer.send(topic_notif, f"A {nombre} le gusto tu publicacion: {titulo}")
	producer.close()

	return topic_notif


@app.route('/get_notifications', methods=['GET'])
def notifications():
	notis = get_notificaciones()[::-1]
	print(notis)
	return 'notis'

def get_notificaciones():
	# Topic con las notificaciones del usuario logueado
	notificaciones = []
	topic_notif = username + '_notificaciones'

	consumer_notificaciones = KafkaConsumer(bootstrap_servers=['localhost:9092'], consumer_timeout_ms=1000)

	# Topic del propio usuario para saber si alguien le dio like o lo sigue 
	notificaciones.append(topic_notif)
	tp_usr = TopicPartition(topic=topic_notif, partition=0)

	consumer_notificaciones.assign([tp_usr])			# Asigna el topic al consumidor

	consumer_notificaciones.seek_to_end(tp_usr)			# Busca el final de la lista
	fin = consumer_notificaciones.position(tp_usr)		# Guarda la posicion del ultimo registro
	consumer_notificaciones.seek_to_beginning(tp_usr)	# Vuelve al inicio de la lista

	# Lista para guardar los registros traidos de kafka
	nt = []
	i = 1
	for notificacion in consumer_notificaciones:		# Itera entre todos los registros del topic seleccionado
#		print(notificacion)
		nt.append('Mensaje numero '+str(i)+' --> '+str(notificacion.value))							# Agrega en la lista todos los registros del topic
		if fin == notificacion.offset:					# Sale del for cuando llega al final de la lista y no espera por nuevos mensajes
			break
		i += 1
	consumer_notificaciones.close()
	return nt
	
def json_serializer(data):
    return json.dumps(data).encode("utf-8")


if __name__=='__main__':
	app.run()