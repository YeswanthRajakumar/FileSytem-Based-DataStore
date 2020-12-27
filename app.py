__author__ = 'Yeswanth Rajakumar'

from  flask import Flask
from  configs import settings,configurations

app =Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

if __name__ == "__main__":
    app.run(host=settings.HOST,port=settings.PORT)