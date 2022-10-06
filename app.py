from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from msilib.schema import tables
from flask import Flask, request, abort
from flask_cors import CORS
import json

from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient, NewTopic
admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id="prueba", api_version=(0, 11, 1))


app = Flask(__name__)
CORS(app)

base_name_topic_auction_product ='auction_product_' 

user = "root" 
password = ""
database_name = "prueba_punto_2"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@localhost/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #para que no tire errores ni warnings

#***********************************************************************************
# ENTITY Y SCHEMA
#***********************************************************************************

ma = Marshmallow(app) #permite definir un esquema para interactuar con la bdf
db = SQLAlchemy(app) #obtenemos una instancia de la bd


class AuctionEntity(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_user_creator = db.Column(db.Integer)
	id_product = db.Column(db.Integer)
	amount_base = db.Column(db.Integer)
	start_date = db.Column(db.DateTime, default = datetime.now())
	end_date = db.Column(db.DateTime)
	id_user_last_offer = db.Column(db.Integer, nullable = True)
	date_last_offer = db.Column(db.DateTime, nullable = True)
	last_amount_offered = db.Column(db.Integer, nullable = True)

	def __init__(self, data): #constructor, se ejecuta cada vez que se instancia la clase
		self.id_user_creator = data['id_user_creator']
		self.id_product = data['id_product']
		self.amount_base = data['amount_base']
		self.end_date = data['end_date']
		self.id_user_last_offer = data['id_user_last_offer']
		self.date_last_offer = data['date_last_offer']
		self.last_amount_offered = data['last_amount_offered']

				#**********************************************************
db.create_all() #lee toda la clase y crea todas las tablas (en este caso 1)
				#**********************************************************

class AuctionSchema(ma.Schema):
	class Meta:
		fields = (
				'id',
				'id_user_creator',
				'id_product',
				'amount_base',
				'start_date',
				'end_date',
				'id_user_last_offer', 
				'date_last_offer',
				'last_amount_offered'
				)

auction_schema = AuctionSchema() #Instanciamos para poder iteractuar con bd para ABM de uno
auctions_schemas = AuctionSchema(many=True) #Para varios/muchos

#***********************************************************************************
# FIN ENTITY Y SCHEMA
#***********************************************************************************

@app.route('/', methods=['GET'])
def hello():
    return "Service (OK)"

#********* uaction *********
@app.route('/new_topic_auction', methods=['POST'])
def new_topic_offer():
	topic_name = base_name_topic_auction_product+str(request.json['id_product'])
	new_topic_auction = add_new_topic_offer() #agrego a la bd
	if(new_topic_auction != None):
		create_topic(topic_name)
		add_message_topic(topic_name, request.json)
		return new_topic_auction #'new topic auction '+topic_name
	else:
		return response_for_error("No se crea la subasta porque ya hay una para el producto")

@app.route('/add_offer', methods=['POST'])
def add_message_offer_to_topic():
	topic_name = base_name_topic_auction_product+str(request.json['id_product'])
	name_product = 'product_'+topic_name #La idea es traerlo desde la base de datos
	request.json['name_product'] = name_product
	auction = getAuctionWithAttributesInCorrectType()
	if(auction != None): #si existe la subasta
		return validaciones_and_mensajes_de_la_subasta(auction, topic_name)
	else:
		return response_for_error('No se agrega la oferta, ya que no existe subasta para el producto')

@app.route('/get_messages_topic_auction', methods=['GET'])
def get_list_messages_topics():
	topic_name = base_name_topic_auction_product+str(request.json['id_product'])
	list_messages = find_list_messages_topic(topic_name)[::-1]
	#print(list_messages)
	return list_messages
#********* fin uaction *********

#-----------------------------
def create_topic(topic_name):
	# Creacion del topic
	topicsList = []
	topicsList.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
	admin_client.create_topics(new_topics=topicsList, validate_only=False)

def add_message_topic(topic_name, message_to_topic, message_info = ""):
	# Se agrega el mensaje al topic 
	producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)
	producer.send(topic_name, message_to_topic)
	producer.close()

	return message_info


def response_for_error(messege_error):
	response_data = {}
	response_data['result'] = None
	response_data['message'] = messege_error

	return response_data

def find_list_messages_topic(topic_name):
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
        #print(topic)
        #print('Mensaje numero '+str(i)+' --> '+str(topic.value))
        listRegisterTopics.append(json.loads(topic.value.decode("utf-8")))		# Agrega en la lista todos los registros del topic
        if fin == topic.offset:					# Sale del for cuando llega al final de la lista y no espera por nuevos mensajes
            break
        i += 1
    consumer_listTopics.close()

    return listRegisterTopics

	
def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def add_new_topic_offer():
	if(AuctionEntity.query.filter(AuctionEntity.id_product == request.json['id_product']).first() == None): # si no hay una subasta Creada para el producto
		data = request.json
		data['id_user_last_offer'] = None
		data['date_last_offer'] = None
		data['last_amount_offered'] = None
		new_auction = AuctionEntity(data) #creo una instancia
		db.session.add(new_auction) #agrego a la bd
		db.session.commit() #termino
		return auction_schema.jsonify(new_auction)
	else:
		return None

def updateAuction(id):
	auction = AuctionEntity.query.get(id)
	auction.id_user_last_offer = request.json['id_offering_user']
	auction.date_last_offer = datetime.now()
	auction.last_amount_offered = request.json['amount_offered']
	db.session.commit() #guardo los cambios

def validacion_y_agregar_primer_oferta(auction, topic_name):
	if(request.json['amount_offered'] >= auction['amount_base']): #si la oferta iguala o supera el importe base
		updateAuction(auction['id']) #actualizo la bd
		return add_message_topic(topic_name, request.json, "Primera oferta agregada correctamente") #agrego la primera oferta
	else:
		return response_for_error('No se agrega por ser una oferta menor al importe base')

def validaciones_and_mensajes_de_la_subasta(auction, topic_name):
	if( auction['end_date'] > datetime.now() ): 
		print(" id_user_last_offer ", auction['id_user_last_offer'])
		if(auction['id_user_last_offer'] == None): #si es la primera  ofertas (nadie ha hecho una oferta 
			return validacion_y_agregar_primer_oferta(auction, topic_name)
		elif( request.json['amount_offered'] > auction['last_amount_offered'] ): #Si no es la primera oferta y supera la última oferta
			updateAuction(auction['id']) #actualizo la bd
			return add_message_topic(topic_name, request.json, "Oferta agregada correctamente") #agrego una oferta
		else:
			return response_for_error('No se agrega porque no supera una ofertaanterior')
	return response_for_error('No se agrega la oferta, ya que la subasta ha finalizado')

def string_to_datetime(str_date):
	str_date = str_date.split("T")[0] #tomo solo la fecha
	#print(" fecha sin hora = ", str_date)
	year = int(str_date.split("-")[0])
	month = int(str_date.split("-")[1])
	day = int(str_date.split("-")[2])

	return datetime(year, month, day)

def getAuctionWithAttributesInCorrectType():
	auction_result_query = db.session.query(AuctionEntity).filter_by( id_product = request.json['id_product'] ).first()
	if(auction_result_query == None):
		return None
	else:
		dump_result_query = auction_schema.dump(auction_result_query)
		auction_response = {}
		auction_response['id'] =  int(dump_result_query['id'])
		auction_response['id_user_creator'] = int(dump_result_query['id_user_creator'])
		auction_response['id_product'] = int(dump_result_query['id_product'])
		auction_response['amount_base'] = int(dump_result_query['amount_base'])
		auction_response['start_date'] = string_to_datetime(dump_result_query['start_date'])
		auction_response['end_date'] = string_to_datetime(dump_result_query['end_date'])
		auction_response['id_user_last_offer'] = None if (dump_result_query['id_user_last_offer']==None) else int(dump_result_query['id_user_last_offer']) #Operador ternario: si era nulo, lo dejo nulo, sino lo parseo 
		auction_response['date_last_offer'] = None if (dump_result_query['date_last_offer']==None) else string_to_datetime(dump_result_query['date_last_offer'])
		auction_response['last_amount_offered'] = None if (dump_result_query['last_amount_offered']==None) else int(dump_result_query['last_amount_offered'])

		return auction_response
#----------------------------- 


if __name__=='__main__':
	app.run() 
	# app.run(debug=True) hace que rinicie luego de un cambio usando "python app.py" 
	# otra opción, app.run(), es correrlo con "pymon app.py", pero solo se actualiza por cambios en app.py y no en otro archivo 