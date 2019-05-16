from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory
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

PROFILE_PICTURE_UPLOAD_FOLDER = './uploads/profile-pictures/'
app.config['PROFILE_PICTURE_UPLOAD_FOLDER'] = PROFILE_PICTURE_UPLOAD_FOLDER

RECIPE_PICTURE_UPLOAD_FOLDER = './uploads/recipe-pictures/'
app.config['RECIPE_PICTURE_UPLOAD_FOLDER'] = RECIPE_PICTURE_UPLOAD_FOLDER

def profile_picture_provider(filename):
    return send_from_directory('uploads/profile-pictures/', filename)
    
def recipe_picture_provider(filename):
    return send_from_directory('uploads/recipe-pictures/', filename)
    
app.add_url_rule('/uploads/images/<path:filename>', endpoint='profile_picture', view_func=profile_picture_provider)

app.add_url_rule('/uploads/images/<path:filename>', endpoint='recipe_picture', view_func=recipe_picture_provider)

def check_login_details(username_input,password_input):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    check_sql = "SELECT id,password FROM users WHERE `username` = '{}'".format(username_input)
    pymysql_cursor.execute(check_sql)
    user_details = pymysql_cursor.fetchone()
    pymysql_cursor.close()
    return user_details

def get_user_recipe_details():
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    
    recipe_details_sql="SELECT `recipes`.`id`,`recipes`.`name` FROM recipes JOIN authors ON `recipes`.`author_id` = `authors`.`id` WHERE `authors`.`user_id` = '{}'".format(session["user_id"])
    pymysql_cursor.execute(recipe_details_sql)
    user_recipe_list=pymysql_cursor.fetchall()
    
    pymysql_cursor.close()
    return user_recipe_list
    
def get_user_dashboard_details(current_user_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    
    user_details_sql="SELECT * FROM users JOIN countries ON users.country_of_origin_id = countries.id WHERE `users`.`id` = '{}'".format(current_user_id)
    pymysql_cursor.execute(user_details_sql)
    user_details=pymysql_cursor.fetchone()
    pymysql_cursor.close()
    
    user_recipe_list=get_user_recipe_details()
    
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
    
    get_photo_lists_sql = "SELECT `uri` FROM `recipe_photos` JOIN `recipes` ON recipe_photos.recipe_id = recipes.id WHERE recipes.id = '{}'".format(article_id)
    pymysql_cursor.execute(get_photo_lists_sql)
    photo_lists_details=pymysql_cursor.fetchall()
    
    pymysql_cursor.close()
    recipe_procedure = recipe_details["recipe_procedure"]
    recipe_procedure_list = recipe_procedure.split(".")
    for i in recipe_procedure_list:
        if i == "":
            recipe_procedure_list.remove(i)
        else:
            pass
    
    recipe_time_details_list = [recipe_time_details["prep_duration_seconds"],recipe_time_details["cook_duration_seconds"],recipe_time_details["ready_in_duration_seconds"]]
    
    # photo_array = []
    # for j in photo_lists_details:
    #     for key,value in j.items():
    #         photo_array.append(str(value))
    
    for j in photo_lists_details:
        photo_uri = j["uri"]
    
    for j in recipe_time_details_list:
        recipe_time_details_list[recipe_time_details_list.index(j)] = str(j)+" seconds"
    return [author_details,recipe_details,ingredient_details,category_lists_details,recipe_procedure_list,recipe_time_details_list,photo_uri]

def recipe_list_helper_function(recipe_lists_article_list_details,category_link_details):
    sorted_category_link_details=sorted(category_link_details, key = lambda k:k['recipe_id'])
    result = {}
    for i in sorted_category_link_details:
        if i["recipe_id"] not in result:
            result.update({i["recipe_id"]:[i["recipe_category_name"],i["category_id"]]})
        else:
            x=i["recipe_id"]
            if isinstance(result.get(x), (list,)):
                category_array = []
                category_array.append(result.get(x))
                category_array.append([i["recipe_category_name"],i["category_id"]])
                result[i["recipe_id"]] = category_array
            else:
                category_array = []
                category_array.append(result.get(i["recipe_id"]))
                category_array.append([i["recipe_category_name"],i["category_id"]])
                result[i["recipe_id"]] = category_array
    
    result_array = [ v for v in result.values() ]
    sorted_recipe_lists_article_list_details=sorted(recipe_lists_article_list_details, key = lambda k:k['post_recipe_id'])
    counter = 0
    for j in sorted_recipe_lists_article_list_details:
        j["post_categories"] = result_array[counter]
        counter+=1
    return sorted_recipe_lists_article_list_details
    
def get_recipe_lists_article_list_details():
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    
    recipe_lists_details_sql = """SELECT recipes.name AS post_recipe_name, posts.date_published AS post_date_published, recipe_photos.uri AS post_photo_uri, posts.number_of_views AS post_number_of_views, 
    recipes.id AS post_recipe_id FROM `posts` JOIN `recipes` ON posts.recipe_id = recipes.id JOIN `recipe_photos` ON recipes.id = recipe_photos.recipe_id"""
    pymysql_cursor.execute(recipe_lists_details_sql)
    recipe_lists_article_list_details=pymysql_cursor.fetchall()
    
    category_link_details_sql = """SELECT categories.id AS category_id,categories.name AS recipe_category_name, recipes.id AS recipe_id FROM `category_lists` JOIN `categories` ON 
    category_lists.category_id = categories.id JOIN `recipes` ON category_lists.recipe_id = recipes.id JOIN `posts` ON recipes.id = posts.recipe_id"""
    pymysql_cursor.execute(category_link_details_sql)
    category_link_details=pymysql_cursor.fetchall()
    
    pymysql_cursor.close()
    
    result = recipe_list_helper_function(recipe_lists_article_list_details,category_link_details)
    return result

def get_user_recipe_lists_article_list_details(current_user_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    
    recipe_lists_details_sql = """SELECT recipes.name AS post_recipe_name, posts.date_published AS post_date_published, recipe_photos.uri AS post_photo_uri,
    posts.number_of_views AS post_number_of_views,recipes.id AS post_recipe_id FROM `posts` JOIN `recipes` ON posts.recipe_id = recipes.id 
    JOIN `recipe_photos` ON recipes.id = recipe_photos.recipe_id JOIN `authors` ON recipes.author_id = authors.id WHERE authors.user_id = '{}'""".format(current_user_id)
    pymysql_cursor.execute(recipe_lists_details_sql)
    recipe_lists_article_list_details=pymysql_cursor.fetchall()
    
    category_link_details_sql = """SELECT categories.id AS category_id,categories.name AS recipe_category_name, recipes.id AS recipe_id FROM `category_lists` 
    JOIN `categories` ON category_lists.category_id = categories.id JOIN `recipes` ON category_lists.recipe_id = recipes.id JOIN `posts` ON recipes.id = posts.recipe_id 
    JOIN `authors` ON recipes.author_id = authors.id WHERE authors.user_id = '{}'""".format(current_user_id)
    pymysql_cursor.execute(category_link_details_sql)
    category_link_details=pymysql_cursor.fetchall()
    
    pymysql_cursor.close()
    
    result = recipe_list_helper_function(recipe_lists_article_list_details,category_link_details)
    return result

def recipe_list_search_function(search_terms):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    search_sql = """SELECT recipes.name AS post_recipe_name, posts.date_published AS post_date_published, recipe_photos.uri AS post_photo_uri, posts.number_of_views AS post_number_of_views,
    recipes.id AS post_recipe_id FROM `posts` JOIN `recipes` ON posts.recipe_id = recipes.id JOIN `recipe_photos` ON recipes.id = recipe_photos.recipe_id WHERE recipes.name LIKE '%{}%'""".format(search_terms)
    pymysql_cursor.execute(search_sql)
    recipe_lists_article_list_details=pymysql_cursor.fetchall()
    
    search_sql_2 = """SELECT categories.id AS category_id,categories.name AS recipe_category_name, recipes.id AS recipe_id FROM `category_lists`
    JOIN `categories` ON category_lists.category_id = categories.id JOIN `recipes` ON category_lists.recipe_id = recipes.id JOIN `posts` ON recipes.id = posts.recipe_id 
    WHERE recipes.name LIKE '%{}%'""".format(search_terms) 
    pymysql_cursor.execute(search_sql_2)
    category_link_details=pymysql_cursor.fetchall()
    
    pymysql_cursor.close()
    result=recipe_list_helper_function(recipe_lists_article_list_details,category_link_details)
    return result

def user_recipe_list_search_function(current_user_id,search_terms):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    
    recipe_lists_details_sql = """SELECT recipes.name AS post_recipe_name, posts.date_published AS post_date_published, recipe_photos.uri AS post_photo_uri, posts.number_of_views AS post_number_of_views,
    recipes.id AS post_recipe_id FROM `posts` JOIN `recipes` ON posts.recipe_id = recipes.id JOIN `recipe_photos` ON recipes.id = recipe_photos.recipe_id JOIN `authors` ON recipes.author_id = authors.id 
    WHERE authors.user_id = '{}' AND recipes.name LIKE '%{}%'""".format(current_user_id,search_terms)
    pymysql_cursor.execute(recipe_lists_details_sql)
    recipe_lists_article_list_details=pymysql_cursor.fetchall()
    
    category_link_details_sql = """SELECT categories.id AS category_id,categories.name AS recipe_category_name, recipes.id AS recipe_id FROM `category_lists`
    JOIN `categories` ON category_lists.category_id = categories.id JOIN `recipes` ON category_lists.recipe_id = recipes.id JOIN `posts` ON recipes.id = posts.recipe_id
    JOIN `authors` ON recipes.author_id = authors.id WHERE authors.user_id = '{}' AND recipes.name LIKE '%{}%'""".format(current_user_id,search_terms)
    pymysql_cursor.execute(category_link_details_sql)
    category_link_details=pymysql_cursor.fetchall()
    
    pymysql_cursor.close()
    
    result = recipe_list_helper_function(recipe_lists_article_list_details,category_link_details)
    return result

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
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    if request.method == "GET":
        country_sql = "SELECT * FROM `countries`"
        pymysql_cursor.execute(country_sql)
        country_list = pymysql_cursor.fetchall()
        return render_template("signup.html",country_list=country_list)
    else:
        error = False
        email_input = request.form["email_input"]
        username_input = request.form["username_input"]
        password_input = request.form["password_input"]
        country_input = request.form["country_input"]
        check_if_user_exists_sql = "SELECT * FROM users WHERE username = '{}'".format(username_input)
        pymysql_cursor.execute(check_if_user_exists_sql)
        existing_user_check = pymysql_cursor.fetchone()
        if(existing_user_check is None):
            hashed_password = bcrypt.generate_password_hash(password_input).decode('utf-8')
            sql = "INSERT INTO users (username,password,email,country_of_origin_id,profile_picture_uri) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")".format(username_input,hashed_password,email_input,country_input,"default-profile-picture.png")
            pymysql_cursor.execute(sql)
            pymysql_connection.commit()
            pymysql_cursor.close()
            session["username"]=username_input
            return redirect(url_for('init'))
        else:
            error = True
            pymysql_cursor.close()
            return render_template("signup.html",error=error)
        
@app.route("/user/recipes")
def recipes():
    if session:
        current_user_id = session["user_id"]
        if request.args.get("search"):
            search_terms = request.args.get("search")
            searched_user_recipe_lists_article_list_details = user_recipe_list_search_function(current_user_id,search_terms)
            return render_template("recipes.html",current_user_id=current_user_id,user_recipe_list=searched_user_recipe_lists_article_list_details)
        else:
            user_recipe_lists_article_list_details = get_user_recipe_lists_article_list_details(current_user_id)
            return render_template("recipes.html",current_user_id=current_user_id,user_recipe_list=user_recipe_lists_article_list_details)
    else:
        return redirect(url_for("init"))

@app.route("/user",methods=["GET","POST"])
def user_dashboard():
    if session:
        current_user_id = session["user_id"]
        if request.method == "GET":
            data = get_user_dashboard_details(current_user_id)
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
            bio_input = request.form["bio_input"]
            user_details_sql="SELECT * FROM users WHERE `id` = '{}'".format(current_user_id)
            pymysql_cursor.execute(user_details_sql)
            user_details = pymysql_cursor.fetchone()
            if((email_input==user_details["email"] and password_input==user_details["password"])or(email_input=="" and password_input=="")):
                no_change_required=True
            elif((email_input==user_details["email"] or email_input=="") and password_input!=""):
                password_changed=True
                update_user_details_sql = "UPDATE users SET password='{}', bio='{}' WHERE id='{}'".format(password_input,bio_input,current_user_id)
            else:
                email_changed=True
                update_user_details_sql = "UPDATE users SET email = '{}', bio='{}' WHERE id='{}'".format(email_input,bio_input,current_user_id)
            pymysql_cursor.execute(update_user_details_sql)
            
            if request.files:
                uploaded_image = request.files["profile-picture-input"]
                if uploaded_image.filename == '':
                    print("no file selected")
                else:
                    f = os.path.join(app.config['PROFILE_PICTURE_UPLOAD_FOLDER'], uploaded_image.filename)
                    uploaded_image.save(f)
                    profile_picture_uri=str(uploaded_image.filename)
                    update_user_photo_sql = "UPDATE users SET profile_picture_uri = '{}' WHERE id = '{}'".format(profile_picture_uri,current_user_id)
                    pymysql_cursor.execute(update_user_photo_sql)
            
            pymysql_connection.commit()
            pymysql_cursor.close()
            return render_template("login.html",no_change_required=no_change_required,password_changed=password_changed,email_changed=email_changed)
    else:
        return redirect(url_for("init"))

@app.route("/recipe_list")
def recipe_list():
    if request.args.get("search"):
        search_terms = request.args.get("search")
        searched_recipe_lists_article_list_details = recipe_list_search_function(search_terms)
        return render_template("recipe_list.html",recipe_list=searched_recipe_lists_article_list_details)
    else:
        recipe_lists_article_list_details = get_recipe_lists_article_list_details()
        return render_template("recipe_list.html",recipe_list=recipe_lists_article_list_details)
    
@app.route("/single/<article_id>")
def article(article_id):
    data = get_article_details(article_id)
    return render_template("single.html",author_details=data[0],recipe_details=data[1],ingredient_details=data[2],category_lists_details=data[3],recipe_procedure_list=data[4],recipe_time_details_list=data[5],photo_uri=data[6])
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
                               
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
