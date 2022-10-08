from flask import request
from kafkaFiles.kafkaFunctions import KafkaFunctions

class IntermediaryProduct():

    def new_topic_product():
        topic_name = str(request.json['id_product'])
        product = {}
        product["old_name"] = request.json["old_name"]
        product["old_price"] = request.json["old_price"]
        product["edition_date"] = None #Después lo vamos a usar para validar
        KafkaFunctions.create_topic(topic_name)
        return KafkaFunctions.add_message_topic(topic_name, product, "Topic creado y mensage agregado correctamente")

    def add_message_to_topic_product():
        topic_name = str(request.json['id_product']) 
        product = {} #Al "add_message_topic" se puede pasar directo el "request.json", pero lo hago así para que no quede guardado el id que es el nombre del topic
        product["old_name"] = request.json["old_name"]
        product["new_name"] = request.json["new_name"] 
        product["old_price"] = request.json["old_price"] 
        product["new_price"] = request.json["new_price"]
        product["edition_date"] = request.json["edition_date"]
        return KafkaFunctions.add_message_topic(topic_name, product, "Agregado correctamente") #agrego

    def get_list_messages_topic_product():
        topic_name = str(request.json['id_product'])
        list_messages = KafkaFunctions.find_list_messages_topic(topic_name)[::-1]
        #print(list_messages)
        return list_messages

IntermediaryProduct()