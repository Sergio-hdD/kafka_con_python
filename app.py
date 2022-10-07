from importsAndConfigsApp import app
from intermediary.intermediaryAuction import IntermediaryAuction


@app.route('/', methods=['GET'])
def hello():
    return "Service (OK)"

#********* uaction *********
@app.route('/new_topic_auction', methods=['POST'])
def new_topic_offer():
	return IntermediaryAuction.new_topic_offer()

@app.route('/add_offer', methods=['POST'])
def add_message_offer_to_topic():
	return IntermediaryAuction.add_message_offer_to_topic()

@app.route('/get_messages_topic_auction', methods=['GET'])
def get_list_messages_topic():
	return IntermediaryAuction.get_list_messages_topic()
#********* fin uaction *********



if __name__=='__main__':
	app.run() 
	# app.run(debug=True) hace que rinicie luego de un cambio usando "python app.py" 
	# otra opción, app.run(), es correrlo con "pymon app.py", pero solo se actualiza por cambios en app.py y no en otro archivo 