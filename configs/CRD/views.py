from flask.views import MethodView
from flask import request,jsonify
from functions import DataStoreCRD

class CreateData(MethodView):
    #initializing DB while invoked
    def __init__(self,db_path):
        self.db_path = db_path

    # Create is POST method
    def post(self):
        try:
            json_data = request.get_json()
        except Exception:
            return jsonify({"STATUS : error , MESSAGE : Incorrect Data format ,Only JSON format acceptable"})

        valid_data,message =  DataStoreCRD().check_create_data(json_data,self.db_path)
        
        # Incase of Invalid Data
        if not valid_data:
            return jsonify({"STATUS": "error", "MESSAGE": message}), 400
        
        #for Valid Data
        return jsonify({"status": "success", "message": message}), 200


