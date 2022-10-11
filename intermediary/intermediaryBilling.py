from asyncio import constants
from flask import request, json
from kafkaFiles.kafkaFunctions import KafkaFunctions
from constants import BASE_CARRITO, BASE_BILL, URL_GRPC_CLIENT
import requests
import json


buyer = {}
buyer['id'] = 1
buyer['name'] = "Nico"
buyer['surname'] = "Borea"

seller = {}
seller['id'] = 2
seller['name'] = "Marian"
seller['surname'] = "Di Gangi"

class IntermediaryBilling():

    # Punto 6
    def new_topic_bill():
        topic_name = BASE_BILL+str(request.json['id_bill'])
        topic_cart_name = BASE_CARRITO+str(request.json['id_cart'])
        bill = {}
        bill["date_issue"] = request.json["date_issue"]        
        productsInCar = KafkaFunctions.find_list_messages_topic(topic_cart_name)[::-1]
        # calculo del total facturado
        total = 0
        for product in productsInCar:
            total += product["price"] * product["amount"]
        bill["bill_total"] = total
        # fin calculo del total facturado
        bill["products_in_cart"] = productsInCar
        bill["buyer"] = buyer
        bill["seller"] = seller
        KafkaFunctions.create_topic(topic_name)
        return KafkaFunctions.add_message_topic(topic_name, bill, "Factura creada correctamente")

    def get_list_messages_topic_bill():
        topic_name = BASE_BILL+str(request.json['id_bill'])
        list_messages = KafkaFunctions.find_list_messages_topic(topic_name)[::-1]
        return list_messages
    
    def new_bill_bd():
        topic_name = BASE_BILL+str(request.json['id_bill'])
        list_messages = KafkaFunctions.find_list_messages_topic(topic_name)[::-1]
        bill = {}
        bill["idUserBuyer"] = list_messages[0]["buyer"]["id"]
        bill["idUserSeller"] = list_messages[0]["seller"]["id"]
        bill["total"] = list_messages[0]["bill_total"]
        bill["datePurchase"] = list_messages[0]["date_issue"]
        print(URL_GRPC_CLIENT+ '/invoice/create')
        res = requests.post(URL_GRPC_CLIENT+ '/invoice/create', bill)
        print(res.json)
       # response = json.loads(res)
        return "hola mundo"
    # Fin punto 6

IntermediaryBilling()

#         idUserBuyer = virtualWallet['idUserBuyer'],
#         idUserSeller = virtualWallet['idUserSeller'],
#         total = virtualWallet['total'],
#         datePurchase = virtualWallet['datePurchase'],