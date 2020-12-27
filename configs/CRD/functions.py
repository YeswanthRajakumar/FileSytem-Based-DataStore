import json
import os
from configurations import DEFAULT_DB_NAME
import fcntl

class DataStoreCRD():

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

    