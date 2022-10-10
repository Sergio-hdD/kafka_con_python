from flask import request
from kafkaFiles.kafkaFunctions import KafkaFunctions
from constants import BASE_AUCTION_PRODUCT, BASE_CARRITO

class IntermediaryCart():

    # Punto 5
    def new_topic_cart():
        topic_name = BASE_CARRITO+str(request.json['id_cart'])
        cart = {}
        cart["id_buyer"] = request.json["id_buyer"]
        cart["id_seller"] = request.json["id_seller"]
        cart["id_product"] = request.json["id_product"]
        cart["product_name"] = request.json["product_name"]
        cart["price"] = request.json["price"]
        cart["amount"] = request.json["amount"]
        # check if the product has an auction
        list_messages = KafkaFunctions.find_list_messages_topic(BASE_AUCTION_PRODUCT+str(cart["id_product"]))[::-1]
        if list_messages == []:
            KafkaFunctions.create_topic(topic_name)
            return KafkaFunctions.add_message_topic(topic_name, cart, "Carrito creado correctamente") #creo el carrito
        else:
            return "No se puede agregar el producto al carrito ya que el mismo se encuentra en subasta"

    def add_message_to_topic_cart():
        topic_name = BASE_CARRITO+str(request.json['id_cart']) 
        product = {}
        product["id_product"] = request.json["id_product"]
        product["id_seller"] = request.json["id_seller"]
        product["product_name"] = request.json["product_name"]
        product["price"] = request.json["price"]
        product["amount"] = request.json["amount"]
        return KafkaFunctions.add_message_topic(topic_name, product, "Producto agregado correctamente") #agrego un producto

    def get_list_messages_topic_cart():
        topic_name = BASE_CARRITO+str(request.json['id_cart'])
        list_messages = KafkaFunctions.find_list_messages_topic(topic_name)[::-1]
        #print(list_messages)
        return list_messages

    # Fin punto 5

IntermediaryCart()