from flask import request
from kafkaFiles.kafkaFunctions import KafkaFunctions

class IntermediaryBilling():

    # Punto 6
    def new_topic_bill():
        topic_name = str(request.json['id_bill'])
        bill = {}
        bill["date_issue"] = request.json["date_issue"]
        bill["bill_total"] = request.json["bill_total"]
        KafkaFunctions.create_topic(topic_name)
        return KafkaFunctions.add_message_topic(topic_name, bill, "Factura creada correctamente")
    # Fin punto 6

IntermediaryBilling()
