from constants import BOOTSTRAP_SERVERS, CLIENT_ID, API_VERSION
from generalFunctions import json, GeneralFunctions
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient, NewTopic
admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS, client_id="prueba", api_version=(1, 1, 1))


class KafkaFunctions():
    
    def create_topic(topic_name):
        # Creacion del topic
        topicsList = []
        topicsList.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
        admin_client.create_topics(new_topics=topicsList, validate_only=False)

    def add_message_topic(topic_name, message_to_topic, message_info = ""):
        # Se agrega el mensaje al topic 
        producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVERS], value_serializer=GeneralFunctions.json_serializer)
        producer.send(topic_name, message_to_topic)
        producer.close()

        return message_info

    def find_list_messages_topic(topic_name):
        listTopics = []
        consumer_listTopics = KafkaConsumer(bootstrap_servers=[BOOTSTRAP_SERVERS], consumer_timeout_ms=1000)
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


KafkaFunctions()