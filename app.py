from importsAndConfigsApp import app
from intermediary.intermediaryAuction import IntermediaryAuction
from intermediary.intermediaryProduct import IntermediaryProduct
from intermediary.intermediaryCart import IntermediaryCart
from intermediary.intermediaryBilling import IntermediaryBilling
from flask import request


@app.route('/', methods=['GET'])
def hello():
    return "Service (OK)"

#********* fin Punto 1 product *********
@app.route('/new_topic_to_product_new', methods=['POST'])
def new_topic_new_product():
	return IntermediaryProduct.new_topic_product()

@app.route('/add_message_update_product', methods=['POST'])
def new_message_update_product(): 
	return IntermediaryProduct.add_message_to_topic_product()

@app.route('/get_messages_topic_product', methods=['GET'])
def get_list_messages_topic_product():
	return IntermediaryProduct.get_list_messages_topic_product()
#********* fin Punto 1 product *********


#********* Punto 2 y 3 auction *********
@app.route('/new_topic_auction', methods=['POST'])
def new_topic_offer():
	return IntermediaryAuction.new_topic_offer()

@app.route('/add_offer', methods=['POST'])
def add_message_offer_to_topic():
	return IntermediaryAuction.add_message_offer_to_topic()

@app.route('/get_messages_topic_auction', methods=['GET'])
def get_list_messages_topic_auction():
	return IntermediaryAuction.get_list_messages_topic_auction()
#********* fin Punto 2 auction *********

#********* Punto 5 cart *********
@app.route('/new_topic_cart', methods=['POST'])
def new_topic_cart():
	return IntermediaryCart.new_topic_cart()

@app.route('/add_message_cart', methods=['POST'])
def new_message_cart(): 
	return IntermediaryCart.add_message_to_topic_cart()

@app.route('/get_messages_topic_cart', methods=['GET'])
def get_list_messages_topic_cart():
	return IntermediaryCart.get_list_messages_topic_cart()
#********* Fin punto 5 cart *********

#********* Punto 6 cart *********
@app.route('/new_topic_bill', methods=['POST'])
def new_topic_bill():
	return IntermediaryBilling.new_topic_bill()

@app.route('/get_messages_topic_bill', methods=['GET'])
def get_list_messages_topic_bill():
	return IntermediaryBilling.get_list_messages_topic_bill()
#********* Fin punto 6 cart *********


if __name__=='__main__':
	app.run(debug=True) 
	# app.run(debug=True) hace que rinicie luego de un cambio usando "python app.py" 
	# otra opción, app.run(), es correrlo con "pymon app.py", pero solo se actualiza por cambios en app.py y no en otro archivo 