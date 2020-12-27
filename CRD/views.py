from flask.views import MethodView
from flask import request,jsonify
from CRD.functions import DataStoreCRD

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
        return jsonify({"STATUS": "success", "MESSAGE": message}), 200


class ReadData(MethodView):
    #initializing DB while invoked
    def __init__(self,db_path):
        self.db_path = db_path

    # Read is GET method
    def get(self):
        key = request.args.get('key')
        # If given is not found
        if key is None: 
            return jsonify({"STATUS": "error", "MESSAGE": "key is required as a query param."}), 400

        # Read data from the datasource with the key if key is Present
        data_found, message = DataStoreCRD().check_read_data(key, self.db_path)

        # If no data with given Key is Found
        if not data_found:
            return jsonify({"status": "error", "message": message}), 404

        return jsonify(message), 200
