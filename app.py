__author__ = 'Yeswanth Rajakumar'

from sys import exit
from flask import Flask
from argparse import ArgumentParser
from configs import settings, configurations
from utils.filehandler import FilePreprocess
from CRD.views import CreateData, ReadData, DeleteData, Home


# Adding/Enabling CommandLineArguments: --datastore
parser = ArgumentParser()
parser.add_argument('--datastore', help='Enter the Datastores absolute path.')
args = parser.parse_args()


# Selecting the DataStore Directory.
# Select user provided datastore path else, select the default path.
if args.datastore:
    db_path = args.datastore
else:
    db_path = configurations.DEFAULT_DB_PATH

# Create a datastore directory.
directory_created = FilePreprocess(db_path).create_folder()
if not directory_created:
    print(f"Permission denied: You can not create the directory(permission error) `{db_path}`.\n")
    exit(0)


app = Flask(__name__)


# Flask App Configurations
app.config['DEBUG'] = settings.DEBUG
app.config['SECRET_KEY'] = settings.SECRET_KEY


# API Endpoints
app.add_url_rule('/', view_func = Home.as_view('show'), methods=['GET'])
app.add_url_rule('/datastore/create', view_func=CreateData.as_view('create', db_path), methods=['POST'])


# Initiates Flask Server
if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)
