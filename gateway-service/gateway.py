from flask import Flask,request,jsonify
from werkzeug.exceptions import NotFound, ServiceUnavailable
import requests

gateway = Flask(__name__)

@gateway.route("/")
def home():
    try:
        response = requests.get("http://127.0.0.1:5000/")
        print(response.json())
        return response.json()
    except:
        raise ServiceUnavailable("The service is unavailable.")


if __name__ == "__main__":
    #server.run(host="0.0.0.0",port=5000)
    gateway.run(port=5001,debug=False)