from flask import Flask,render_template,request,redirect,url_for,session
from flask_bcrypt import check_password_hash,Bcrypt,generate_password_hash
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
    return render_template("index.html",session=session)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
        username_input = request.form["username_input"]
        password_input = request.form["password_input"]
        check_sql = "SELECT id,password FROM users WHERE `username` = '{}'".format(username_input)
        pymysql_cursor.execute(check_sql)
        user_details = pymysql_cursor.fetchone()
        pymysql_cursor.close()
        if user_details is not None:
            stored_password = user_details["password"]
            if bcrypt.check_password_hash(stored_password,password_input):
                session["username"] = username_input
                session["user_id"] = user_details["id"]
                return redirect(url_for("init"))
            else:
                return render_template("login.html",incorrect_password=True)
        else:
            return render_template("login.html",user_does_not_exist=True)

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username',None)
    return redirect(url_for("init"))
    
@app.route("/user_creation",methods=["GET","POST"])
def user_creation():
    if request.method == "GET":
        pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
        return render_template("signup.html")
    else:
        error = False
        pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
        email_input = request.form["email_input"]
        username_input = request.form["username_input"]
        password_input = request.form["password_input"]
        check_if_user_exists_sql = "SELECT * FROM users WHERE username = '{}'".format(username_input)
        pymysql_cursor.execute(check_if_user_exists_sql)
        existing_user_check = pymysql_cursor.fetchone()
        if(existing_user_check is None):
            hashed_password = bcrypt.generate_password_hash(password_input).decode('utf-8')
            sql = "INSERT INTO users (username,password,email) VALUES (\"{}\",\"{}\",\"{}\")".format(username_input,hashed_password,email_input)
            pymysql_cursor.execute(sql)
            pymysql_connection.commit()
            pymysql_cursor.close()
            session["username"]=username_input
            return redirect(url_for('init'))
        else:
            error = True
            pymysql_cursor.close()
            return render_template("signup.html",error=error)
        
@app.route("/user/recipe_creator",methods=["GET","POST"])
def recipe_creator():
    if request.method == "GET":
        current_user_id = session["user_id"]
        return render_template("recipe_creator.html",current_user_id=current_user_id)
    else:
        return("ASD")

@app.route("/user",methods=["GET","POST"])
def user_dashboard():
    if request.method == "GET":
        pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
        user_details_sql="SELECT * FROM users WHERE `id` = '{}'".format(session["user_id"])
        recipe_details_sql="SELECT `recipes`.`id`,`recipes`.`name` FROM recipes JOIN authors ON `recipes`.`author_id` = `authors`.`id` WHERE `authors`.`user_id` = '{}'".format(session["user_id"])
        pymysql_cursor.execute(user_details_sql)
        user_details=pymysql_cursor.fetchone()
        pymysql_cursor.execute(recipe_details_sql)
        user_recipe_list=pymysql_cursor.fetchall()
        pymysql_cursor.close()
        return render_template("user_dashboard.html",user_details=user_details,user_recipe_list=user_recipe_list)
    else:
        pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
        no_change_required=False
        password_changed=False
        email_changed=False
        email_input = request.form["email_input"]
        password_input = request.form["password_input"]
        user_details_sql="SELECT * FROM users WHERE `id` = '{}'".format(session["user_id"])
        pymysql_cursor.execute(user_details_sql)
        user_details = pymysql_cursor.fetchone()
        if((email_input==user_details["email"] and password_input==user_details["password"])or(email_input=="" and password_input=="")):
            no_change_required=True
        elif((email_input==user_details["email"] or email_input=="") and password_input!=""):
            password_changed=True
            update_user_details_sql = "UPDATE users SET password='{}' WHERE id='{}'".format(password_input,session["user_id"])
        else:
            email_changed=True
            update_user_details_sql = "UPDATE users SET email = '{}' WHERE id='{}'".format(email_input,session["user_id"])
        pymysql_cursor.execute(update_user_details_sql)
        pymysql_connection.commit()
        pymysql_cursor.close()
        return render_template("login.html",no_change_required=no_change_required,password_changed=password_changed,email_changed=email_changed)

@app.route("/recipe_list")
def recipe_list():
    return render_template("recipe_list.html")
    
@app.route("/single")
def article():
    return render_template("single.html")
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
