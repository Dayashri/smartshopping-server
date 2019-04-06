from flask import Flask, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_cors import CORS
import json
import requests


app = Flask(__name__)
CORS(app, resources=r'/*', headers='Content-Type')
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/hackInventory"

mongo = PyMongo(app)

@app.route('/')
def index():
    return 'welcome to store inventory'
	
@app.route('/mostviewed')
def mostviewed():
    allmodeldetails= dumps(mongo.db.storeinventory.find({}).sort([('searchcount', -1)]).limit(2)  );
    return allmodeldetails

@app.route('/modeldetails/<string:modelid>')
def modeldetails(modelid):
    mongo.db.storeinventory.update_one({"modelid":modelid},{"$inc":{"searchcount":1}})
    modeldetails= dumps(mongo.db.storeinventory.find({"modelid":modelid}));
    return modeldetails

if __name__ == '__main__':
     app.run(debug=True,port=8080)