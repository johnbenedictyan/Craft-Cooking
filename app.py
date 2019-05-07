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

def check_login_details(username_input,password_input):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    check_sql = "SELECT id,password FROM users WHERE `username` = '{}'".format(username_input)
    pymysql_cursor.execute(check_sql)
    user_details = pymysql_cursor.fetchone()
    pymysql_cursor.close()
    return user_details
    
def get_user_dashboard_details():
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    user_details_sql="SELECT * FROM users WHERE `id` = '{}'".format(session["user_id"])
    recipe_details_sql="SELECT `recipes`.`id`,`recipes`.`name` FROM recipes JOIN authors ON `recipes`.`author_id` = `authors`.`id` WHERE `authors`.`user_id` = '{}'".format(session["user_id"])
    pymysql_cursor.execute(user_details_sql)
    user_details=pymysql_cursor.fetchone()
    pymysql_cursor.execute(recipe_details_sql)
    user_recipe_list=pymysql_cursor.fetchall()
    pymysql_cursor.close()
    return_array = [user_details,user_recipe_list]
    return return_array

def get_article_details(article_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    
    get_author_details_sql = "SELECT users.username,users.id FROM `authors` JOIN `recipes` ON recipes.author_id = authors.id JOIN `users` ON authors.user_id = users.id WHERE recipes.id = '{}'".format(article_id)
    pymysql_cursor.execute(get_author_details_sql)
    author_details=pymysql_cursor.fetchone()
    
    get_recipe_details_sql = "SELECT recipes.serves,recipes.name,recipes.recipe_procedure FROM `recipes` WHERE recipes.id = '{}'".format(article_id)
    pymysql_cursor.execute(get_recipe_details_sql)
    recipe_details=pymysql_cursor.fetchone()
    
    get_recipe_time_details_sql = "SELECT recipes.ready_in_duration_seconds,recipes.prep_duration_seconds,recipes.cook_duration_seconds FROM `recipes` WHERE recipes.id = '{}'".format(article_id)
    pymysql_cursor.execute(get_recipe_time_details_sql)
    recipe_time_details=pymysql_cursor.fetchone()
    
    get_ingredient_details_sql="SELECT name,ingredient_amount FROM `ingredients` JOIN `ingredient_lists` ON ingredients.id = ingredient_lists.ingredient_id WHERE ingredient_lists.recipe_id = '{}'".format(article_id)
    pymysql_cursor.execute(get_ingredient_details_sql)
    ingredient_details=pymysql_cursor.fetchall()
    
    get_category_lists_sql = "SELECT name FROM `categories` JOIN `category_lists` ON categories.id = category_lists.category_id WHERE category_lists.recipe_id = '{}'".format(article_id)
    pymysql_cursor.execute(get_category_lists_sql)
    category_lists_details=pymysql_cursor.fetchall()
    
    pymysql_cursor.close()
    recipe_procedure = recipe_details["recipe_procedure"]
    recipe_procedure_list = recipe_procedure.split(".")
    for i in recipe_procedure_list:
        if i == "":
            recipe_procedure_list.remove(i)
        else:
            pass
    
    recipe_time_details_list = [recipe_time_details["prep_duration_seconds"],recipe_time_details["cook_duration_seconds"],recipe_time_details["ready_in_duration_seconds"]]
    for j in recipe_time_details_list:
        recipe_time_details_list[recipe_time_details_list.index(j)] = str(j)+" seconds"
    return [author_details,recipe_details,ingredient_details,category_lists_details,recipe_procedure_list,recipe_time_details_list]

@app.route("/")
def init():
    return render_template("index.html",session=session)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username_input = request.form["username_input"]
        password_input = request.form["password_input"]
        user_details = check_login_details(username_input,password_input)
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
        
@app.route("/user/recipes",methods=["GET","POST"])
def recipes():
    if request.method == "GET":
        current_user_id = session["user_id"]
        return render_template("recipes.html",current_user_id=current_user_id)
    else:
        return("ASD")

@app.route("/user",methods=["GET","POST"])
def user_dashboard():
    if request.method == "GET":
        data = get_user_dashboard_details()
        user_details = data[0]
        user_recipe_list = data[1]
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
    
@app.route("/single/<article_id>")
def article(article_id):
    data = get_article_details(article_id)
    return render_template("single.html",author_details=data[0],recipe_details=data[1],ingredient_details=data[2],category_lists_details=data[3],recipe_procedure_list=data[4],recipe_time_details_list = data[5])
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
