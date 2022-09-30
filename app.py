from flask import Flask
from flask_cors import CORS

# Para la creacion del topic 
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient, NewTopic
import json

app = Flask(__name__)
CORS(app)

admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id="prueba", api_version=(0, 10, 1))

topic_name = 'idProduc_topic_9'


@app.route('/', methods=['GET'])
def hello():
    return "Service (OK)"

@app.route('/new_topic', methods=['GET','POST'])
def create_topic():
	# Creacion del topic
	topicsList = []
	topicsList.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
	admin_client.create_topics(new_topics=topicsList, validate_only=False)

	return 'new topic '+topic_name


@app.route('/new_partition' , methods=['GET','POST'])
def create_partition():
	# Creacion de la particion dentro del topic
#	producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)
#	producer.send(topic_name, "otro mensaje")
#	producer.close()

	return 'new partition metodo anulado porque en realidad generaba otro topic/mensaje'

@app.route('/add_message', methods=['POST'])
def create_message_to_topic():
	nombre_producto = 'product_1'
	cliente_nombre = 'client_name'
	importe = 1000
	# Se agrega el mensaje al topic 
	producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)
	producer.send(topic_name, f"El cliente {cliente_nombre} ofrecre {importe} por el producto {nombre_producto}")
	producer.close()

	return 'added message to '+topic_name


@app.route('/get_topics', methods=['GET'])
def getListTopics():
	list_topics = get_listTopics()[::-1]
	print(list_topics)
	return 'topics'

def get_listTopics():
	listTopics = []

	consumer_listTopics = KafkaConsumer(bootstrap_servers=['localhost:9092'], consumer_timeout_ms=1000)

	# se trae el topic para saber si hubo cambios 
	listTopics.append(topic_name)
	one_topic = TopicPartition(topic=topic_name, partition=0)

	consumer_listTopics.assign([one_topic])			# Asigna el topic al consumidor

	consumer_listTopics.seek_to_end(one_topic)			# Busca el final de la lista
	fin = consumer_listTopics.position(one_topic)		# Guarda la posicion del ultimo registro
	consumer_listTopics.seek_to_beginning(one_topic)	# Vuelve al inicio de la lista

	# Lista para guardar los registros traidos de kafka
	listRegisterTopics = []
	i = 1
	for topic in consumer_listTopics:		# Itera entre todos los registros (mensajes) del topic seleccionado
#		print(topic)
#       print('Mensaje numero '+str(i)+' --> '+str(topic.value))
		listRegisterTopics.append(topic)		# Agrega en la lista todos los registros del topic
		if fin == topic.offset:					# Sale del for cuando llega al final de la lista y no espera por nuevos mensajes
			break
		i += 1
	consumer_listTopics.close()
	return listRegisterTopics
	
def json_serializer(data):
    return json.dumps(data).encode("utf-8")


if __name__=='__main__':
	app.run()