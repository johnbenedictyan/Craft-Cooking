from flask import Flask,render_template,request,redirect
from werkzeug.utils import secure_filename
import pymongo
import os
import pymysql
from bson import ObjectId
db_url = "mongodb://dbuser:asd123@cluster0-shard-00-00-6c1o3.mongodb.net:27017,cluster0-shard-00-01-6c1o3.mongodb.net:27017,cluster0-shard-00-02-6c1o3.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"
mongo_connection = pymongo.MongoClient(db_url)

pymysql_connection = pymysql.connect(host="localhost",
                             user = "johnbenedict",
                             password="",
                             db="craft_cooking")
                             
app = Flask(__name__)
@app.route("/")
def init():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/user_creation",methods=["GET","POST"])
def user_creation():
    if request.method == "GET":
        pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
        return render_template("signup.html")
    else:
        successful_signup = False
        error = False
        pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
        email_input = request.form["email_input"]
        username_input = request.form["username_input"]
        password_input = request.form["password_input"]
        check_if_user_exists_sql = "SELECT * FROM users WHERE username = '{}'".format(username_input)
        pymysql_cursor.execute(check_if_user_exists_sql)
        existing_user_check = pymysql_cursor.fetchone()
        if(existing_user_check==None):
            sql = "INSERT INTO users (username,password,email) VALUES (\"{}\",\"{}\",\"{}\")".format(username_input,password_input,email_input)
            pymysql_cursor.execute(sql)
            successful_signup = True
        else:
            error = True
        pymysql_cursor.close()
        return render_template("signup.html",successful_signup=successful_signup,error=error)
        
@app.route("/recipe_editor/<recipe_id>",methods=["GET","POST"])
def edit(recipe_id):
    return("Welcome!")

@app.route("/recipe_creator",methods=["GET","POST"])
def recipe_creator():
    return("Welcome!")

@app.route("/recipe_deletor/<recipe_id>",methods=["GET","POST"])
def recipe_deletor():
    return("Welcome!")

@app.route("/recipe_list")
def recipe_list():
    return("Welcome!")
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)