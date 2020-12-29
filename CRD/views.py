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
    def __init__(self, db_path):
        self.db_path = db_path

    def get(self):
        key = request.args.get('key')
        if key is None:
            return jsonify({"status": "error", "message": "key is required as a query param."}), 400

        # Read data from the datasource with the key(data index).
        data_found, message = DataStoreCRD().check_read_data(key, self.db_path)
        if not data_found:
            return jsonify({"status": "error", "message": message}), 404
        return jsonify(message), 200

class DeleteData(MethodView):
    def __init__(self, db_path):
        self.db_path = db_path
    


class Home(MethodView):
         def __init__(self):
            self.value = 1

         def get(self):
                return  "<h1>Welcome to Home Page</h1> <span><b>(Use postman)</b></span> <p>Create :  /datastore/create</p> <p> Read :  /datastore/read</p> <p> Delete :  /datastore/delete</p>"