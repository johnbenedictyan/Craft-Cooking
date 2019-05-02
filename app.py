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

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
        user_does_not_exist = False
        incorrect_password = False
        successful_login = False
        username_input = request.form["username_input"]
        password_input = request.form["password_input"]
        check_if_user_exists_sql = "SELECT * FROM users WHERE username = '{}'".format(username_input)
        check_if_password_is_correct_sql = "SELECT username,id FROM users WHERE username = '{}' AND password= '{}'".format(username_input,password_input)
        pymysql_cursor.execute(check_if_user_exists_sql)
        existing_user_check = pymysql_cursor.fetchone()
        pymysql_cursor.execute(check_if_password_is_correct_sql)
        correct_password_check = pymysql_cursor.fetchone()
        if(existing_user_check==None):
            user_does_not_exist=True
            return render_template("login.html",user_does_not_exist=user_does_not_exist)
        elif(correct_password_check==None):
            incorrect_password=True
            return render_template("login.html",incorrect_password=incorrect_password)
        else:
            successful_login = True
            user_details=correct_password_check
            print(user_details)
            return render_template("index.html",successful_login=successful_login,user_details=user_details)

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
        
@app.route("/user/<current_user_id>/recipe_editor/<recipe_id>",methods=["GET","POST"])
def edit(current_user_id,recipe_id):
    return("Welcome!")

@app.route("/user/<current_user_id>/recipe_creator",methods=["GET","POST"])
def recipe_creator(current_user_id):
    return("Welcome!")

@app.route("/user/<current_user_id>/recipe_deletor/<recipe_id>",methods=["GET","POST"])
def recipe_deletor(current_user_id,recipe_id):
    return("Welcome!")

@app.route("/user/<current_user_id>/recipe_list")
def recipe_list(current_user_id):
    return("Welcome!")
    
@app.route("/user/<current_user_id>")
def user_dashboard(current_user_id):
    return("Welcome!")
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)