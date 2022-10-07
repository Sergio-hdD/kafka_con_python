from datetime import datetime
import json

class GeneralFunctions():

    def response_for_error(messege_error):
        response_data = {}
        response_data['result'] = None
        response_data['message'] = messege_error

        return response_data

    def string_to_datetime(str_date):
        str_date = str_date.split("T")[0] #tomo solo la fecha
		#print(" fecha sin hora = ", str_date)
        year = int(str_date.split("-")[0])
        month = int(str_date.split("-")[1])
        day = int(str_date.split("-")[2])
        
        return datetime(year, month, day)

    def json_serializer(data):
        return json.dumps(data).encode("utf-8")

    def base_auction_product():
        return 'auction_product_' 


GeneralFunctions()