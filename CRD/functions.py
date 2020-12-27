import json
import os
from configs.configurations import DEFAULT_DB_NAME
import fcntl
from datetime import datetime, timedelta
from dateutil.parser import parse


class DataStoreCRD():
    def check_time_to_live(self, value):
        # Checks how long the data is accessible.

        created_time = value['CreatedAt']

        # Parse the datetime from the string date.
        created_time = parse(created_time)

        time_to_live = value['Time-To-Live']


        # Default time to live 

        # if time_to_live is None:
        #     time_to_live = 100000

        if time_to_live is not None:
            # Calculate the data expire time.
            expired_datetime = created_time + timedelta(seconds=time_to_live)

            # Calculate the remaining seconds of expired time(may/may not expired) from current time.
            remaining_seconds = (expired_datetime - datetime.now()).total_seconds()

            if remaining_seconds <= 0:
                return False

        return value


    def read_delete_preprocess(self, key, db_path):
            datastore = os.path.join(db_path, DEFAULT_DB_NAME)

            # Check for datastore existance.
            if not os.path.isfile(datastore):
                return False, "Empty DataStore. Data not found for the key."

            # Read previous datastore data if exists.
            with open(datastore) as f:
                # Make sure single process only allowed to access the file at a time.
                # Locking file.
                fcntl.flock(f, fcntl.LOCK_EX)
                data = json.load(f)
                # Releasing the file lock.
                fcntl.flock(f, fcntl.LOCK_UN)

            # Check for the input key available in data.
            if key not in data.keys():
                return False, "No data found for the key provided."

            # Check for the data for the key is active or inactive.
            target = data[key]
            target_active = self.check_time_to_live(target)
            if not target_active:
                return False, "Requested data is expired for the key."

            return True, data
    

    def check_read_data(self, key ,db_path):
             # Read data from the datasource for the given key.
             status,message = self.read_delete_preprocess(key, db_path)
             if not status:
                 return status,message
            
             data = message[key]

             del data['CreatedAt']

             return status,data


    def check_create_data(self, json_data, db_path):

            if not isinstance(json_data, dict):
                return False, "Incorrect Data format. Only JSON object  is acceptable."

            # Check for request data size. If size is greater than 1GB ignore the data.
            data_obj = json.dumps(json_data)

            # Data Greater Than one GB

            if len(data_obj) > 1000000000:
                return False, "DataStore limit is exceeded than 1GB size."

            for key, value in json_data.items():
                # Check for key in data for 32 char length.
                if len(key) > 32:
                    return False, "The keys must be in 32 characters length."

                # Check for value in data whether it is JSON object or not.
                if not isinstance(value, dict):
                    return False, "The values must be in JSON object formats."

                value_obj = json.dumps(value)

                # Check for value JSON object is 16KB or less in size.
                if len(value_obj) > 16384:
                    return False, "The values must be in 16KB size."

            # Checks if DataStore exists.
            # If datastore exists append existing datastore,
            # else create a new datastore with data inserted.
            datastore = os.path.join(db_path, DEFAULT_DB_NAME)
            data = {}
            if os.path.isfile(datastore):
                with open(datastore) as f:
                    # Make sure single process only allowed to access the file at a time.
                    # Locking file.
                    fcntl.flock(f, fcntl.LOCK_EX)
                    data = json.load(f)
                    # Releasing the file lock.
                    fcntl.flock(f, fcntl.LOCK_UN)

                    # Check if file size exceeded 1GB size.
                    prev_data_obj = json.dumps(data)
                    if len(prev_data_obj) >= 1000000000:
                        return False, "File Size Exceeded 1GB after Additiion of Current."


            # Check any key present in previous datastore data.
            # If present return Error message
            '''
            # for key in json_data.keys():
            #     if key in data.keys():
            #         return False, "Key already exist in DataStore."
            '''
            
            have_key = any(x in json_data.keys() for x in data.keys())
            if have_key:
                return False, "Key already exist in DataStore. Try With Different Key"

      

    