from datetime import datetime
import json
import requests
from constants import URL_GRPC_CLIENT, URL_REST_SERVER

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

    def stringDate_to_datetime(str_date):
        year = int(str_date.split("-")[0])
        month = int(str_date.split("-")[1])
        day = int(str_date.split("-")[2])
        
        return datetime(year, month, day)

    def json_serializer(data):
        return json.dumps(data).encode("utf-8")

    def base_auction_product():
        return 'auction_product_' 

    def isMonitor(username):
        validate = False

        res = requests.post(URL_GRPC_CLIENT+'/findUserByUsername', json={
            "username" : "admin",
            "password" : "admin",
            "usernameToFind" : username
        })
        if(json.loads(res.content)['user'] != {} and json.loads(res.content)['user']['role'] == 'MONITOR'):
            validate = True

        return validate

    def getUserById(id):
        res = requests.get(URL_REST_SERVER+'/api/users/byId', json={
            "id" : id
        })

        return json.loads(res.content)

        

GeneralFunctions()