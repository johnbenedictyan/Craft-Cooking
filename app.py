from flask import Flask,render_template,request,redirect
from werkzeug.utils import secure_filename
import pymongo
import os
from bson import ObjectId
db_url = "mongodb://dbuser:asd123@cluster0-shard-00-00-6c1o3.mongodb.net:27017,cluster0-shard-00-01-6c1o3.mongodb.net:27017,cluster0-shard-00-02-6c1o3.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"
connection = pymongo.MongoClient(db_url)
allergens_collection = connection["tgs_codeinstitude_project3_db"]["allergens"]
authors_collection = connection["tgs_codeinstitude_project3_db"]["authors"]
posts_collection = connection["tgs_codeinstitude_project3_db"]["posts"]
recipes_collection = connection["tgs_codeinstitude_project3_db"]["recipes"]
users_collection = connection["tgs_codeinstitude_project3_db"]["users"]

app = Flask(__name__)
@app.route("/")
def init():
    return ("Welcome!")

@app.route("/login")
def login():
    return ("Welcome!")

@app.route("/user_creation",methods=["GET","POST"])
def user_creation():
    return("Welcome!")

@app.route("/recipe_editor/<recipe_id>",methods=["GET","POST"])
def edit(recipe_id):
    return("Welcome!")

@app.route("/recipe_creator",methods=["GET","POST"])
def recipe_creator():
    return("Welcome!")

@app.route("/recipe_deletor/<recipe_id>",methods=["GET","POST"])
def recipe_deletor():
    return("Welcome!")
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)