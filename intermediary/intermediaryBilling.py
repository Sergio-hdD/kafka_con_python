from asyncio import constants
from itertools import product
from math import prod
from flask import request, json
from kafkaFiles.kafkaFunctions import KafkaFunctions
from constants import BASE_CARRITO, BASE_BILL, URL_GRPC_CLIENT
import requests
import json
from generalFunctions import GeneralFunctions

class IntermediaryBilling():

    # Punto 6
    def new_topic_bill():
        topic_name = BASE_BILL+str(request.json['id_bill'])
        topic_cart_name = BASE_CARRITO+str(request.json['id_cart'])
        id_seller = request.json['id_seller']
        id_buyer =  request.json['id_buyer']
        bill = {}
        bill["date_issue"] = request.json["date_issue"]        
        cart = KafkaFunctions.find_list_messages_topic(topic_cart_name)[::-1]
        # calculo del total facturado
        total = 0
        products = []
        if cart == []:
            return "No se crea la factura, porque que no se agregaron productos o no existe el carrito"
        else:
            for itemCart in cart:
                if(itemCart['id_seller'] == id_seller):
                    total += itemCart["price"] * itemCart["amount"]

                    product = {}
                    product["id_product"] = itemCart["id_product"]
                    product["product_name"] = itemCart["product_name"]
                    product["price"] = itemCart["price"]
                    product["amount"] = itemCart["amount"]

                    products.append(product)

            bill["bill_total"] = total
            # fin calculo del total facturado
            bill["products_in_cart"] = products
            bill["buyer"] = GeneralFunctions.getUserById(id_buyer)
            bill["seller"] = GeneralFunctions.getUserById(id_seller)
            KafkaFunctions.create_topic(topic_name)
            return KafkaFunctions.add_message_topic(topic_name, bill, "Factura creada correctamente")

    def get_list_messages_topic_bill():
        topic_name = BASE_BILL+str(request.json['id_bill'])
        list_messages = KafkaFunctions.find_list_messages_topic(topic_name)[::-1]
        return list_messages
    # Fin punto 6

    #Punto 7    
    def new_bill_bd():
        topic_name = BASE_BILL+str(request.json['id_bill'])
        list_messages = KafkaFunctions.find_list_messages_topic(topic_name)[::-1]
        bill = {}
        bill["idUserBuyer"] = list_messages[0]["buyer"]["id"]
        bill["idUserSeller"] = list_messages[0]["seller"]["id"]
        bill["total"] = list_messages[0]["bill_total"]
        bill["datePurchase"] = list_messages[0]["date_issue"]
        res = requests.post(URL_GRPC_CLIENT+'/invoice/create', json=bill)
        return json.loads(res.content)
    #Fin punto 7
    
IntermediaryBilling()
