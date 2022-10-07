from datetime import datetime
from schemas.auctionSchema import AuctionSchema
from generalFunctions import GeneralFunctions
from kafkaFiles.kafkaFunctions import KafkaFunctions
from entities.auctionEntity import AuctionEntity
from flask import request
from constants import BASE_AUCTION_PRODUCT

db = AuctionEntity.prepare_table_auction_and_get_db()

db.create_all() #creo todas las tablas (en este caso 1)

auction_schema = AuctionSchema() #Instanciamos para poder iteractuar con bd para ABM de uno
auctions_schemas = AuctionSchema(many=True) #Para varios/muchos


class IntermediaryAuction():

    def new_topic_offer():
        topic_name = BASE_AUCTION_PRODUCT+str(request.json['id_product'])
        new_topic_auction = IntermediaryAuction.add_new_topic_offer() #agrego a la bd
        if(new_topic_auction != None):
            KafkaFunctions.create_topic(topic_name)
            KafkaFunctions.add_message_topic(topic_name, request.json)
            return new_topic_auction #'new topic auction '+topic_name
        else:
            return GeneralFunctions.response_for_error("No se crea la subasta porque ya hay una para el producto")

    def add_message_offer_to_topic():
        topic_name = BASE_AUCTION_PRODUCT+str(request.json['id_product'])
        name_product = 'product_'+topic_name #La idea es traerlo desde la base de datos
        request.json['name_product'] = name_product
        auction = IntermediaryAuction.getAuctionWithAttributesInCorrectType()
        if(auction != None): #si existe la subasta
            return IntermediaryAuction.validaciones_and_mensajes_de_la_subasta(auction, topic_name)
        else:
            return GeneralFunctions.response_for_error('No se agrega la oferta, ya que no existe subasta para el producto')

    def get_list_messages_topic():
        topic_name = BASE_AUCTION_PRODUCT+str(request.json['id_product'])
        list_messages = KafkaFunctions.find_list_messages_topic(topic_name)[::-1]
        #print(list_messages)
        return list_messages

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


    def validaciones_and_mensajes_de_la_subasta(auction, topic_name):
        if( auction['end_date'] > datetime.now() ): 
            print(" id_user_last_offer ", auction['id_user_last_offer'])
            if(auction['id_user_last_offer'] == None): #si es la primera  ofertas (nadie ha hecho una oferta 
                return IntermediaryAuction.validacion_y_agregar_primer_oferta(auction, topic_name)
            elif( request.json['amount_offered'] > auction['last_amount_offered'] ): #Si no es la primera oferta y supera la última oferta
                IntermediaryAuction.updateAuction(auction['id']) #actualizo la bd
                return KafkaFunctions.add_message_topic(topic_name, request.json, "Oferta agregada correctamente") #agrego una oferta
            else:
                return GeneralFunctions.response_for_error('No se agrega porque no supera una ofertaanterior')
        return GeneralFunctions.response_for_error('No se agrega la oferta, ya que la subasta ha finalizado')

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
            auction_response['start_date'] = GeneralFunctions.string_to_datetime(dump_result_query['start_date'])
            auction_response['end_date'] = GeneralFunctions.string_to_datetime(dump_result_query['end_date'])
            auction_response['id_user_last_offer'] = None if (dump_result_query['id_user_last_offer']==None) else int(dump_result_query['id_user_last_offer']) #Operador ternario: si era nulo, lo dejo nulo, sino lo parseo 
            auction_response['date_last_offer'] = None if (dump_result_query['date_last_offer']==None) else GeneralFunctions.string_to_datetime(dump_result_query['date_last_offer'])
            auction_response['last_amount_offered'] = None if (dump_result_query['last_amount_offered']==None) else int(dump_result_query['last_amount_offered'])

            return auction_response
    def updateAuction(id):
        auction = AuctionEntity.query.get(id)
        auction.id_user_last_offer = request.json['id_offering_user']
        auction.date_last_offer = datetime.now()
        auction.last_amount_offered = request.json['amount_offered']
        db.session.commit() #guardo los cambios

    def validacion_y_agregar_primer_oferta(auction, topic_name):
        if(request.json['amount_offered'] >= auction['amount_base']): #si la oferta iguala o supera el importe base
            IntermediaryAuction.updateAuction(auction['id']) #actualizo la bd
            return KafkaFunctions.add_message_topic(topic_name, request.json, "Primera oferta agregada correctamente") #agrego la primera oferta
        else:
            return GeneralFunctions.response_for_error('No se agrega por ser una oferta menor al importe base')

IntermediaryAuction()