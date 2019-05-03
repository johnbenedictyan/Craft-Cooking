from flask import Flask,render_template,request,redirect,url_for,session
from flask_bcrypt import Bcrypt
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
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)
@app.route("/")
def init():
    session['user']='user'
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
        check_if_user_exists_sql = "SELECT * FROM users WHERE `username` = '{}'".format(username_input)
        check_if_password_is_correct_sql = "SELECT username,id FROM users WHERE `username` = '{}' AND `password`= '{}'".format(username_input,password_input)
        pymysql_cursor.execute(check_if_user_exists_sql)
        existing_user_check = pymysql_cursor.fetchone()
        pymysql_cursor.execute(check_if_password_is_correct_sql)
        user_details = pymysql_cursor.fetchone()
        pymysql_cursor.close()
        if(existing_user_check==None):
            user_does_not_exist=True
            return render_template("login.html",user_does_not_exist=user_does_not_exist)
        elif(user_details==None):
            incorrect_password=True
            return render_template("login.html", incorrect_password=incorrect_password)
        else:
            successful_login = True
            return render_template("index.html",successful_login=successful_login,user_details=user_details)

@app.route("/logout")
def logout():
    return redirect(url_for("init"))
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
            pymysql_connection.commit()
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
    
@app.route("/user/<current_user_id>",methods=["GET","POST"])
def user_dashboard(current_user_id):
    if request.method == "GET":
        pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
        user_details_sql="SELECT * FROM users WHERE `id` = '{}'".format(current_user_id)
        recipe_details_sql="SELECT `recipes`.`id`,`recipes`.`name` FROM recipes LEFT JOIN authors ON `recipes`.`author_id` = `authors`.`id` WHERE `authors`.`user_id` = '{}'".format(current_user_id)
        pymysql_cursor.execute(user_details_sql)
        user_details = pymysql_cursor.fetchone()
        pymysql_cursor.execute(recipe_details_sql)
        user_recipe_list=pymysql_cursor.fetchall()
        print(user_recipe_list)
        pymysql_cursor.close()
        print(user_details)
        return render_template("user_dashboard.html",user_details=user_details,user_recipe_list=user_recipe_list)
    else:
        pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
        no_change_required=False
        password_changed=False
        email_changed=False
        email_input = request.form["email_input"]
        password_input = request.form["password_input"]
        user_details_sql="SELECT * FROM users WHERE `id` = '{}'".format(current_user_id)
        pymysql_cursor.execute(user_details_sql)
        user_details = pymysql_cursor.fetchone()
        if((email_input==user_details["email"] and password_input==user_details["password"])or(email_input=="" and password_input=="")):
            no_change_required=True
        elif((email_input==user_details["email"] or email_input=="") and password_input!=""):
            password_changed=True
            update_user_details_sql = "UPDATE users SET password='{}' WHERE id='{}'".format(password_input,current_user_id)
        else:
            email_changed=True
            update_user_details_sql = "UPDATE users SET email = '{}' WHERE id='{}'".format(email_input,current_user_id)
        pymysql_cursor.execute(update_user_details_sql)
        pymysql_connection.commit()
        pymysql_cursor.close()
        return render_template("login.html",no_change_required=no_change_required,password_changed=password_changed,email_changed=email_changed)
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
