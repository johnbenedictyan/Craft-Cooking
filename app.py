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
    
app.add_url_rule('/uploads/profile-pictures/<path:filename>', endpoint='profile_picture', view_func=profile_picture_provider)

app.add_url_rule('/uploads/recipe-pictures/<path:filename>', endpoint='recipe_picture', view_func=recipe_picture_provider)

pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)

def check_login_details(username_input,password_input):
    
    check_sql = "SELECT id,password FROM users WHERE `username` = %s"
    check_input = (username_input)
    pymysql_cursor.execute(check_sql,check_input)
    user_details = pymysql_cursor.fetchone()
    
    return user_details

def get_user_recipe_details(current_user_id):
    recipe_details_sql="SELECT `recipes`.`id`,`recipes`.`name` FROM recipes JOIN authors ON `recipes`.`author_id` = `authors`.`id` WHERE `authors`.`user_id` = %s"
    recipe_details_input = (current_user_id)
    pymysql_cursor.execute(recipe_details_sql,recipe_details_input)
    user_recipe_list=pymysql_cursor.fetchall()
    
    return user_recipe_list
    
def get_user_dashboard_details(current_user_id):
    user_details_sql="SELECT * FROM users JOIN countries ON users.country_of_origin_id = countries.id WHERE `users`.`id` = %s"
    user_details_input=(current_user_id)
    pymysql_cursor.execute(user_details_sql,user_details_input)
    user_details=pymysql_cursor.fetchone()
    
    user_recipe_list=get_user_recipe_details(current_user_id)
    
    return_array = [user_details,user_recipe_list]
    return return_array

def get_post_categories(post_id):
    
    
    get_allergen_lists_sql = "SELECT allergens.id AS allergen_id,allergens.name AS allergen_name FROM `allergens` JOIN `allergen_lists` ON allergens.id = allergen_lists.allergen_id WHERE allergen_lists.recipe_id = %s"
    get_allergen_lists_input = (post_id)
    pymysql_cursor.execute(get_allergen_lists_sql,get_allergen_lists_input)
    allergen_lists_details=pymysql_cursor.fetchall()
    
    get_cooking_style_lists_sql = "SELECT cooking_styles.id AS cooking_style_id,cooking_styles.name AS cooking_style_name FROM `cooking_styles` JOIN `cooking_style_lists` ON cooking_styles.id = cooking_style_lists.cooking_style_id WHERE cooking_style_lists.recipe_id = %s"
    get_cooking_style_lists_input = (post_id)
    pymysql_cursor.execute(get_cooking_style_lists_sql,get_cooking_style_lists_input)
    cooking_style_lists_details=pymysql_cursor.fetchall()
    
    get_cuisine_lists_sql = "SELECT cuisines.id AS cuisine_id,cuisines.name AS cuisine_name FROM `cuisines` JOIN `cuisine_lists` ON cuisines.id = cuisine_lists.cuisine_id WHERE cuisine_lists.recipe_id = %s"
    get_cuisine_lists_input = (post_id)
    pymysql_cursor.execute(get_cuisine_lists_sql,get_cuisine_lists_input)
    cuisine_lists_details=pymysql_cursor.fetchall()
    
    get_diet_health_type_lists_sql = "SELECT diet_health_types.id AS diet_health_type_id,diet_health_types.name AS diet_health_type_name FROM `diet_health_types` JOIN `diet_health_type_lists` ON diet_health_types.id = diet_health_type_lists.diet_health_type_id WHERE diet_health_type_lists.recipe_id = %s"
    get_diet_health_type_lists_input = (post_id)
    pymysql_cursor.execute(get_diet_health_type_lists_sql,get_diet_health_type_lists_input)
    diet_health_type_lists_details=pymysql_cursor.fetchall()
    
    get_dish_type_lists_sql = "SELECT dish_types.id AS dish_type_id,dish_types.name AS dish_type_name FROM `dish_types` JOIN `dish_type_lists` ON dish_types.id = dish_type_lists.dish_type_id WHERE dish_type_lists.recipe_id = %s"
    get_dish_type_lists_input = (post_id)
    pymysql_cursor.execute(get_dish_type_lists_sql,get_dish_type_lists_input)
    dish_type_lists_details=pymysql_cursor.fetchall()
    
    get_meal_type_lists_sql = "SELECT meal_types.id AS meal_type_id,meal_types.name AS meal_type_name FROM `meal_types` JOIN `meal_type_lists` ON meal_types.id = meal_type_lists.meal_type_id WHERE meal_type_lists.recipe_id = %s"
    get_meal_type_lists_input = (post_id)
    pymysql_cursor.execute(get_meal_type_lists_sql,get_meal_type_lists_input)
    meal_type_lists_details=pymysql_cursor.fetchall()
    
    
    
    category_lists_details = [
        allergen_lists_details,
        cooking_style_lists_details,
        cuisine_lists_details,
        diet_health_type_lists_details,
        dish_type_lists_details,
        meal_type_lists_details
        ]
    
    return category_lists_details
    
def get_post_details(post_id):
    
    get_author_details_sql = "SELECT users.username,users.id,users.profile_picture_uri,users.bio FROM `authors` JOIN `recipes` ON recipes.author_id = authors.id JOIN `users` ON authors.user_id = users.id WHERE recipes.id = %s"
    get_author_details_input = (post_id)
    pymysql_cursor.execute(get_author_details_sql,get_author_details_input)
    author_details=pymysql_cursor.fetchone()
    
    get_recipe_details_sql = "SELECT recipes.serves,recipes.name,recipes.recipe_procedure FROM `recipes` WHERE recipes.id = %s"
    get_recipe_details_input = (post_id)
    pymysql_cursor.execute(get_recipe_details_sql,get_recipe_details_input)
    recipe_details=pymysql_cursor.fetchone()
    
    get_recipe_time_details_sql = "SELECT recipes.ready_in_duration_seconds,recipes.prep_duration_seconds,recipes.cook_duration_seconds FROM `recipes` WHERE recipes.id = %s"
    get_recipe_time_details_input = (post_id)
    pymysql_cursor.execute(get_recipe_time_details_sql,get_recipe_time_details_input)
    recipe_time_details=pymysql_cursor.fetchone()
    
    get_ingredient_details_sql="SELECT name,ingredient_amount FROM `ingredients` JOIN `ingredient_lists` ON ingredients.id = ingredient_lists.ingredient_id WHERE ingredient_lists.recipe_id = %s"
    get_ingredient_details_input = (post_id)
    pymysql_cursor.execute(get_ingredient_details_sql,get_ingredient_details_input)
    ingredient_details=pymysql_cursor.fetchall()
    
    get_photo_lists_sql = "SELECT `uri` FROM `recipe_photos` JOIN `recipes` ON recipe_photos.recipe_id = recipes.id WHERE recipes.id = %s"
    get_photo_lists_input = (post_id)
    pymysql_cursor.execute(get_photo_lists_sql,get_photo_lists_input)
    photo_details=pymysql_cursor.fetchone()
    
    
    recipe_procedure = recipe_details["recipe_procedure"]
    recipe_procedure_list = recipe_procedure.split(".")
    for i in recipe_procedure_list:
        if i == "":
            recipe_procedure_list.remove(i)
        else:
            pass
    
    recipe_time_details_list = [recipe_time_details["prep_duration_seconds"],recipe_time_details["cook_duration_seconds"],recipe_time_details["ready_in_duration_seconds"]]
    
    photo_uri = photo_details["uri"]
    
    for j in recipe_time_details_list:
        recipe_time_details_list[recipe_time_details_list.index(j)] = str(j)+" seconds"
        
        
    return [author_details,recipe_details,ingredient_details,recipe_procedure_list,recipe_time_details_list,photo_uri]

def get_post_categories_for_recipe_editor(post_id):
    
    
    cat_allergen = []
    get_allergen_lists_sql = "SELECT allergens.id AS allergen_id FROM `allergens` JOIN `allergen_lists` ON allergens.id = allergen_lists.allergen_id WHERE allergen_lists.recipe_id = %s"
    get_allergen_lists_input = (post_id)
    pymysql_cursor.execute(get_allergen_lists_sql,get_allergen_lists_input)
    allergen_lists_details=pymysql_cursor.fetchall()
    for i in allergen_lists_details:
        cat_allergen.append(i["allergen_id"])
    
    
    cat_cooking_style = []
    get_cooking_style_lists_sql = "SELECT cooking_styles.id AS cooking_style_id FROM `cooking_styles` JOIN `cooking_style_lists` ON cooking_styles.id = cooking_style_lists.cooking_style_id WHERE cooking_style_lists.recipe_id = %s"
    get_cooking_style_lists_input = (post_id)
    pymysql_cursor.execute(get_cooking_style_lists_sql,get_cooking_style_lists_input)
    cooking_style_lists_details=pymysql_cursor.fetchall()
    for i in cooking_style_lists_details:
        cat_cooking_style.append(i["cooking_style_id"])
        
        
    cat_cuisine = []
    get_cuisine_lists_sql = "SELECT cuisines.id AS cuisine_id FROM `cuisines` JOIN `cuisine_lists` ON cuisines.id = cuisine_lists.cuisine_id WHERE cuisine_lists.recipe_id = %s"
    get_cuisine_lists_input = (post_id)
    pymysql_cursor.execute(get_cuisine_lists_sql,get_cuisine_lists_input)
    cuisine_lists_details=pymysql_cursor.fetchall()
    for i in cuisine_lists_details:
        cat_cuisine.append(i["cuisine_id"])
        
        
    cat_diet_health_type = []
    get_diet_health_type_lists_sql = "SELECT diet_health_types.id AS diet_health_type_id FROM `diet_health_types` JOIN `diet_health_type_lists` ON diet_health_types.id = diet_health_type_lists.diet_health_type_id WHERE diet_health_type_lists.recipe_id = %s"
    get_diet_health_type_lists_input = (post_id)
    pymysql_cursor.execute(get_diet_health_type_lists_sql,get_diet_health_type_lists_input)
    diet_health_type_lists_details=pymysql_cursor.fetchall()
    for i in diet_health_type_lists_details:
        cat_diet_health_type.append(i["diet_health_type_id"])
        
        
    cat_dish_type = []
    get_dish_type_lists_sql = "SELECT dish_types.id AS dish_type_id FROM `dish_types` JOIN `dish_type_lists` ON dish_types.id = dish_type_lists.dish_type_id WHERE dish_type_lists.recipe_id = %s"
    get_dish_type_lists_input = (post_id)
    pymysql_cursor.execute(get_dish_type_lists_sql,get_dish_type_lists_input)
    dish_type_lists_details=pymysql_cursor.fetchall()
    for i in dish_type_lists_details:
        cat_dish_type.append(i["dish_type_id"])
        
        
    cat_meal_type = []
    get_meal_type_lists_sql = "SELECT meal_types.id AS meal_type_id FROM `meal_types` JOIN `meal_type_lists` ON meal_types.id = meal_type_lists.meal_type_id WHERE meal_type_lists.recipe_id = %s"
    get_meal_type_lists_input = (post_id)
    pymysql_cursor.execute(get_meal_type_lists_sql,get_meal_type_lists_input)
    meal_type_lists_details=pymysql_cursor.fetchall()
    for i in meal_type_lists_details:
        cat_meal_type.append(i["meal_type_id"])
        
        
    
    
    category_lists_details = [
        cat_allergen,
        cat_cooking_style,
        cat_cuisine,
        cat_diet_health_type,
        cat_dish_type,
        cat_meal_type
        ]
    
    return category_lists_details
    
def get_recipe_details_for_recipe_editor(post_id):
    
    
    get_recipe_details_sql = "SELECT recipes.serves,recipes.name,recipes.recipe_procedure FROM `recipes` WHERE recipes.id = %s"
    get_recipe_details_input = (post_id)
    pymysql_cursor.execute(get_recipe_details_sql,get_recipe_details_input)
    recipe_details=pymysql_cursor.fetchone()
    
    get_recipe_time_details_sql = "SELECT recipes.ready_in_duration_seconds,recipes.prep_duration_seconds,recipes.cook_duration_seconds FROM `recipes` WHERE recipes.id = %s"
    get_recipe_time_details_input = (post_id)
    pymysql_cursor.execute(get_recipe_time_details_sql,get_recipe_time_details_input)
    recipe_time_details=pymysql_cursor.fetchone()
    
    get_ingredient_details_sql="SELECT name,ingredient_amount FROM `ingredients` JOIN `ingredient_lists` ON ingredients.id = ingredient_lists.ingredient_id WHERE ingredient_lists.recipe_id = %s"
    get_ingredient_details_input = (post_id)
    pymysql_cursor.execute(get_ingredient_details_sql,get_ingredient_details_input)
    ingredient_details=pymysql_cursor.fetchall()
    
    get_photo_sql = "SELECT `uri` FROM `recipe_photos` JOIN `recipes` ON recipe_photos.recipe_id = recipes.id WHERE recipes.id = %s"
    get_photo_input = (post_id)
    pymysql_cursor.execute(get_photo_sql,get_photo_input)
    photo_uri=pymysql_cursor.fetchone()
    
    current_post_categories_list = get_post_categories_for_recipe_editor(post_id)
    
    get_recipe_creator_form_details_allergens_sql = "SELECT id,name FROM allergens"
    pymysql_cursor.execute(get_recipe_creator_form_details_allergens_sql)
    allergens_form_list = pymysql_cursor.fetchall()
    
    get_recipe_creator_form_details_cooking_styles_sql = "SELECT id,name FROM cooking_styles"
    pymysql_cursor.execute(get_recipe_creator_form_details_cooking_styles_sql)
    cooking_styles_form_list = pymysql_cursor.fetchall()
    
    get_recipe_creator_form_details_cuisines_sql = "SELECT id,name FROM cuisines"
    pymysql_cursor.execute(get_recipe_creator_form_details_cuisines_sql)
    cuisines_form_list = pymysql_cursor.fetchall()
    
    get_recipe_creator_form_details_diet_health_types_sql = "SELECT id,name FROM diet_health_types"
    pymysql_cursor.execute(get_recipe_creator_form_details_diet_health_types_sql)
    diet_health_types_form_list = pymysql_cursor.fetchall()
    
    get_recipe_creator_form_details_dish_types_sql = "SELECT id,name FROM dish_types"
    pymysql_cursor.execute(get_recipe_creator_form_details_dish_types_sql)
    dish_types_form_list = pymysql_cursor.fetchall()
    
    get_recipe_creator_form_details_meal_types_sql = "SELECT id,name FROM meal_types"
    pymysql_cursor.execute(get_recipe_creator_form_details_meal_types_sql)
    meal_types_form_list = pymysql_cursor.fetchall()
    
    
    
    all_categories_list = [allergens_form_list,cooking_styles_form_list,cuisines_form_list,diet_health_types_form_list,dish_types_form_list,meal_types_form_list]
    
    recipe_procedure = recipe_details["recipe_procedure"]
    recipe_procedure_list = recipe_procedure.split(".")
    for c,v in enumerate(recipe_procedure_list):
        if v == "":
            recipe_procedure_list.remove(v)
        else:
            recipe_procedure_list[c] += "."
    
    current_post_details = [recipe_details,ingredient_details,recipe_procedure_list,recipe_time_details,photo_uri["uri"]]
    
    result  = {
        "current_post_details":current_post_details,
        "current_post_categories":current_post_categories_list,
        "all_available_categories":all_categories_list
    }
    return result
    
def recipe_list_helper_function(recipe_lists_post_list_details):
    for i in recipe_lists_post_list_details:
        categories = get_post_categories(int(i['post_id']))
        i["allergens"] = categories[0]
        i["cooking_styles"] = categories[1]
        i["cuisines"] = categories[2]
        i["diet_health_types"] = categories[3]
        i["dish_types"] = categories[4]
        i["meal_types"] = categories[5]
        
    return recipe_lists_post_list_details
    
def get_recipe_lists_post_list_details(): 
    
    
    recipe_lists_details_sql = """SELECT recipes.name AS post_recipe_name, posts.date_published AS post_date_published, recipe_photos.uri AS post_photo_uri, posts.number_of_views AS post_number_of_views, 
    recipes.id AS post_recipe_id, posts.id AS post_id FROM `posts` JOIN `recipes` ON posts.recipe_id = recipes.id JOIN `recipe_photos` ON recipes.id = recipe_photos.recipe_id"""
    pymysql_cursor.execute(recipe_lists_details_sql)
    recipe_lists_post_list_details=pymysql_cursor.fetchall()
    
    result = recipe_list_helper_function(recipe_lists_post_list_details)
    
    
    
    return result

def get_user_recipe_lists_post_list_details(current_user_id): 
    
    
    recipe_lists_details_sql = """SELECT recipes.name AS post_recipe_name, posts.date_published AS post_date_published, recipe_photos.uri AS post_photo_uri,
    posts.number_of_views AS post_number_of_views,recipes.id AS post_recipe_id, posts.id AS post_id  FROM `posts` JOIN `recipes` ON posts.recipe_id = recipes.id 
    JOIN `recipe_photos` ON recipes.id = recipe_photos.recipe_id JOIN `authors` ON recipes.author_id = authors.id WHERE authors.user_id = %s """
    recipe_lists_details_input = (current_user_id)
    pymysql_cursor.execute(recipe_lists_details_sql,recipe_lists_details_input)
    recipe_lists_post_list_details=pymysql_cursor.fetchall()
    
    
    
    result = recipe_list_helper_function(recipe_lists_post_list_details)
    return result
    
def recipe_list_search_function(search_terms): 
    
    search_sql = """SELECT recipes.name AS post_recipe_name, posts.date_published AS post_date_published, recipe_photos.uri AS post_photo_uri, posts.number_of_views AS post_number_of_views,
    recipes.id AS post_recipe_id, posts.id AS post_id FROM `posts` JOIN `recipes` ON posts.recipe_id = recipes.id JOIN `recipe_photos` ON recipes.id = recipe_photos.recipe_id WHERE recipes.id = %s
    """
    sql_1 = "SELECT recipes.id AS recipe_id FROM `recipes` WHERE recipes.name LIKE %s"
    sql_2 = "SELECT cuisine_lists.recipe_id FROM `cuisine_lists` JOIN `cuisines` ON cuisine_lists.cuisine_id = cuisines.id WHERE cuisines.name LIKE %s"
    sql_3 = "SELECT cooking_style_lists.recipe_id FROM `cooking_style_lists` JOIN `cooking_styles` ON cooking_style_lists.cooking_style_id = cooking_styles.id WHERE cooking_styles.name LIKE %s"
    sql_4 = "SELECT diet_health_type_lists.recipe_id FROM `diet_health_type_lists` JOIN `diet_health_types` ON diet_health_type_lists.diet_health_type_id = diet_health_types.id WHERE diet_health_types.name LIKE %s"
    sql_5 = "SELECT dish_type_lists.recipe_id FROM `dish_type_lists` JOIN `dish_types` ON dish_type_lists.dish_type_id = dish_types.id WHERE dish_types.name LIKE %s"
    sql_6 = "SELECT meal_type_lists.recipe_id FROM `meal_type_lists` JOIN `meal_types` ON meal_type_lists.meal_type_id = meal_types.id WHERE meal_types.name LIKE %s"
    
    search_input = ("%" + search_terms +"%")
    
    pymysql_cursor.execute(sql_1,search_input)
    result_1=pymysql_cursor.fetchall()
    
    pymysql_cursor.execute(sql_2,search_input)
    result_2=pymysql_cursor.fetchall()
    
    pymysql_cursor.execute(sql_3,search_input)
    result_3=pymysql_cursor.fetchall()
    
    pymysql_cursor.execute(sql_4,search_input)
    result_4=pymysql_cursor.fetchall()
    
    pymysql_cursor.execute(sql_5,search_input)
    result_5=pymysql_cursor.fetchall()
    
    pymysql_cursor.execute(sql_6,search_input)
    result_6=pymysql_cursor.fetchall()
    
    recipe_input_array = [result_1,result_2,result_3,result_4,result_5,result_6]
    recipe_result_array = []
    for i in recipe_input_array:
        if i is not tuple:
            for j in i:
                if j not in recipe_result_array:
                    recipe_result_array.append(j["recipe_id"])
    
    final_recipe_list_result = []
    for k in recipe_result_array:
        search_input = k
        pymysql_cursor.execute(search_sql,k)
        search_result = pymysql_cursor.fetchone()
        final_recipe_list_result.append(search_result)
        
    result=recipe_list_helper_function(final_recipe_list_result)
    
    
    return result
    
def user_recipe_list_search_function(current_user_id,search_terms): 
    
    search_sql = """SELECT recipes.name AS post_recipe_name, posts.date_published AS post_date_published, recipe_photos.uri AS post_photo_uri, posts.number_of_views AS post_number_of_views,
    recipes.id AS post_recipe_id, posts.id AS post_id FROM `posts` JOIN `recipes` ON posts.recipe_id = recipes.id JOIN `recipe_photos` ON recipes.id = recipe_photos.recipe_id JOIN `authors` ON recipes.author_id = authors.id WHERE recipes.id = %s AND authors.user_id = %s
    """
    sql_1 = "SELECT recipes.id AS recipe_id FROM `recipes` WHERE recipes.name LIKE %s"
    sql_2 = "SELECT cuisine_lists.recipe_id FROM `cuisine_lists` JOIN `cuisines` ON cuisine_lists.cuisine_id = cuisines.id WHERE cuisines.name LIKE %s"
    sql_3 = "SELECT cooking_style_lists.recipe_id FROM `cooking_style_lists` JOIN `cooking_styles` ON cooking_style_lists.cooking_style_id = cooking_styles.id WHERE cooking_styles.name LIKE %s"
    sql_4 = "SELECT diet_health_type_lists.recipe_id FROM `diet_health_type_lists` JOIN `diet_health_types` ON diet_health_type_lists.diet_health_type_id = diet_health_types.id WHERE diet_health_types.name LIKE %s"
    sql_5 = "SELECT dish_type_lists.recipe_id FROM `dish_type_lists` JOIN `dish_types` ON dish_type_lists.dish_type_id = dish_types.id WHERE dish_types.name LIKE %s"
    sql_6 = "SELECT meal_type_lists.recipe_id FROM `meal_type_lists` JOIN `meal_types` ON meal_type_lists.meal_type_id = meal_types.id WHERE meal_types.name LIKE %s"
    
    search_input = ("%" + search_terms +"%")
    
    pymysql_cursor.execute(sql_1,search_input)
    result_1=pymysql_cursor.fetchall()
    
    pymysql_cursor.execute(sql_2,search_input)
    result_2=pymysql_cursor.fetchall()
    
    pymysql_cursor.execute(sql_3,search_input)
    result_3=pymysql_cursor.fetchall()
    
    pymysql_cursor.execute(sql_4,search_input)
    result_4=pymysql_cursor.fetchall()
    
    pymysql_cursor.execute(sql_5,search_input)
    result_5=pymysql_cursor.fetchall()
    
    pymysql_cursor.execute(sql_6,search_input)
    result_6=pymysql_cursor.fetchall()
    
    recipe_input_array = [result_1,result_2,result_3,result_4,result_5,result_6]
    recipe_result_array = []
    for i in recipe_input_array:
        if i is not tuple:
            for j in i:
                if j not in recipe_result_array:
                    recipe_result_array.append(j["recipe_id"])
    
    final_recipe_list_result = []
    for k in recipe_result_array:
        search_input = (k,current_user_id)
        pymysql_cursor.execute(search_sql,search_input)
        search_result = pymysql_cursor.fetchone()
        if search_result:
            final_recipe_list_result.append(search_result)
    
    
    result=recipe_list_helper_function(final_recipe_list_result)
    
    return result

def check_if_user_is_an_author(current_user_id):
    
    get_author_id_sql = "SELECT id FROM authors WHERE authors.user_id = %s"
    get_author_id_input = (current_user_id)
    pymysql_cursor.execute(get_author_id_sql,get_author_id_input)
    author_id = int(pymysql_cursor.fetchone()["id"])
    
    return author_id

def get_recipe_creator_form_details():
    
    
    get_recipe_creator_form_details_allergens_sql = "SELECT id,name FROM allergens"
    pymysql_cursor.execute(get_recipe_creator_form_details_allergens_sql)
    allergens_form_list = pymysql_cursor.fetchall()
    
    get_recipe_creator_form_details_cooking_styles_sql = "SELECT id,name FROM cooking_styles"
    pymysql_cursor.execute(get_recipe_creator_form_details_cooking_styles_sql)
    cooking_styles_form_list = pymysql_cursor.fetchall()
    
    get_recipe_creator_form_details_cuisines_sql = "SELECT id,name FROM cuisines"
    pymysql_cursor.execute(get_recipe_creator_form_details_cuisines_sql)
    cuisines_form_list = pymysql_cursor.fetchall()
    
    get_recipe_creator_form_details_diet_health_types_sql = "SELECT id,name FROM diet_health_types"
    pymysql_cursor.execute(get_recipe_creator_form_details_diet_health_types_sql)
    diet_health_types_form_list = pymysql_cursor.fetchall()
    
    get_recipe_creator_form_details_dish_types_sql = "SELECT id,name FROM dish_types"
    pymysql_cursor.execute(get_recipe_creator_form_details_dish_types_sql)
    dish_types_form_list = pymysql_cursor.fetchall()
    
    get_recipe_creator_form_details_meal_types_sql = "SELECT id,name FROM meal_types"
    pymysql_cursor.execute(get_recipe_creator_form_details_meal_types_sql)
    meal_types_form_list = pymysql_cursor.fetchall()
    
    
    
    result = [allergens_form_list,cooking_styles_form_list,cuisines_form_list,diet_health_types_form_list,dish_types_form_list,meal_types_form_list]
    
    return result
    
def recipe_creator_ingredient_list_sorting_function():
    return None
    
def recipe_updater_ingredient_list():
    return None
    
def recipe_creator_big_function(recipe_title,author_id,prep_time,cook_time,ready_in_time,serves_number,recipe_procedure,recipe_picture_uri,allergens,cooking_styles,cuisines,diet_health_types,dish_types,meal_types):
    
    final_recipe_procedure_result = ""
    for i in recipe_procedure:
        if(i[len(i)-1]=="."):
            final_recipe_procedure_result+=i
        else:
            i += "."
            final_recipe_procedure_result+=i
            
    recipe_creation_sql = "INSERT INTO recipes (id,name,author_id,prep_duration_seconds,cook_duration_seconds,ready_in_duration_seconds,serves,recipe_procedure) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
    recipe_creation_input = (None,recipe_title,author_id,prep_time,cook_time,ready_in_time,serves_number,final_recipe_procedure_result)
    pymysql_cursor.execute(recipe_creation_sql,recipe_creation_input)
    pymysql_connection.commit()
    
    find_lastest_recipe_sql = "SELECT id FROM recipes ORDER BY id DESC LIMIT 1"
    pymysql_cursor.execute(find_lastest_recipe_sql)
    lastest_recipe_id = int(pymysql_cursor.fetchone()["id"])
    
    recipe_photo_creation_sql = "INSERT INTO recipe_photos (id,uri,recipe_id) VALUES (%s,%s,%s);"
    recipe_photo_creation_input = (None,recipe_picture_uri,lastest_recipe_id)
    pymysql_cursor.execute(recipe_photo_creation_sql,recipe_photo_creation_input)
    pymysql_connection.commit()
    
    post_creation_sql = "INSERT INTO posts (id,date_published,number_of_views,recipe_id) VALUES (%s,CURRENT_DATE(),%s,%s);"
    post_creation_input = (None,0,lastest_recipe_id)
    pymysql_cursor.execute(post_creation_sql,post_creation_input)
    pymysql_connection.commit()
    
    for i in allergens:
        recipe_creation_allergen_sql = "INSERT INTO allergen_lists (recipe_id,allergen_id) VALUES (%s,%s);"
        recipe_creation_allergen_input = (lastest_recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_allergen_sql,recipe_creation_allergen_input)
    
    for j in cooking_styles:
        recipe_creation_cooking_styles_sql = "INSERT INTO cooking_style_lists (recipe_id,cooking_style_id) VALUES (%s,%s);"
        recipe_creation_cooking_styles_input = (lastest_recipe_id,int(j))
        pymysql_cursor.execute(recipe_creation_cooking_styles_sql,recipe_creation_cooking_styles_input)
        
    for k in cuisines:
        recipe_creation_cuisines_sql = "INSERT INTO cuisine_lists (recipe_id,cuisine_id) VALUES (%s,%s);"
        recipe_creation_cuisines_input = (lastest_recipe_id,int(k))
        pymysql_cursor.execute(recipe_creation_cuisines_sql,recipe_creation_cuisines_input)
        
    for l in diet_health_types:
        recipe_creation_diet_health_types_sql = "INSERT INTO diet_health_type_lists (recipe_id,diet_health_type_id) VALUES (%s,%s);"
        recipe_creation_diet_health_types_input = (lastest_recipe_id,int(l))
        pymysql_cursor.execute(recipe_creation_diet_health_types_sql,recipe_creation_diet_health_types_input)
        
    for m in dish_types:
        recipe_creation_dish_types_sql = "INSERT INTO dish_type_lists (recipe_id,dish_type_id) VALUES (%s,%s);"
        recipe_creation_dish_types_input = (lastest_recipe_id,int(m))
        pymysql_cursor.execute(recipe_creation_dish_types_sql,recipe_creation_dish_types_input)
        
    for n in meal_types:
        recipe_creation_meal_types_sql = "INSERT INTO meal_type_lists (recipe_id,meal_type_id) VALUES (%s,%s);"
        recipe_creation_meal_types_input = (lastest_recipe_id,int(n))
        pymysql_cursor.execute(recipe_creation_meal_types_sql,recipe_creation_meal_types_input)
    
    pymysql_connection.commit()
    
    return True

def recipe_updater_big_function(recipe_title,prep_time,cook_time,ready_in_time,serves_number,recipe_procedure,recipe_picture_uri,allergens,cooking_styles,cuisines,diet_health_types,dish_types,meal_types,recipe_id,change_photo_indicator):
    
    final_recipe_procedure_result = ""
    for i in recipe_procedure:
        if(i[len(i)-1]=="."):
            final_recipe_procedure_result+=i
        else:
            i += "."
            final_recipe_procedure_result+=i
    
    print(final_recipe_procedure_result)
    deletion_recipe_id = (recipe_id)
    
    recipe_update_sql = "UPDATE recipes SET name=%s,prep_duration_seconds=%s,cook_duration_seconds=%s,ready_in_duration_seconds=%s,serves=%s,recipe_procedure=%s WHERE recipes.id=%s;"
    recipe_update_input = (recipe_title,prep_time,cook_time,ready_in_time,serves_number,final_recipe_procedure_result,recipe_id)
    print(recipe_update_input)
    pymysql_cursor.execute(recipe_update_sql,recipe_update_input)
    pymysql_connection.commit()
    
    if change_photo_indicator is True:
        recipe_photo_update_sql = "UPDATE recipe_photos SET uri = %s WHERE recipe_photos.recipe_id = %s;"
        recipe_photo_update_input = (recipe_picture_uri,recipe_id)
        pymysql_cursor.execute(recipe_photo_update_sql,recipe_photo_update_input)
        pymysql_connection.commit()
    
    allergen_list_deletion_sql = "DELETE FROM `allergen_lists` WHERE allergen_lists.recipe_id = %s;"
    pymysql_cursor.execute(allergen_list_deletion_sql,deletion_recipe_id)
    
    for i in allergens:
        recipe_creation_allergen_sql = "INSERT INTO allergen_lists (recipe_id,allergen_id) VALUES (%s,%s);"
        recipe_creation_allergen_input = (recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_allergen_sql,recipe_creation_allergen_input)
    
    cooking_style_list_deletion_sql = "DELETE FROM `cooking_style_lists` WHERE cooking_style_lists.recipe_id = %s;"
    pymysql_cursor.execute(cooking_style_list_deletion_sql,deletion_recipe_id)
    
    for j in cooking_styles:
        recipe_creation_cooking_styles_sql = "INSERT INTO cooking_style_lists (recipe_id,cooking_style_id) VALUES (%s,%s);"
        recipe_creation_cooking_styles_input = (recipe_id,int(j))
        pymysql_cursor.execute(recipe_creation_cooking_styles_sql,recipe_creation_cooking_styles_input)
    
    cuisine_list_deletion_sql = "DELETE FROM `cuisine_lists` WHERE cuisine_lists.recipe_id = %s;"    
    pymysql_cursor.execute(cuisine_list_deletion_sql,deletion_recipe_id)
    
    for k in cuisines:
        recipe_creation_cuisines_sql = "INSERT INTO cuisine_lists (recipe_id,cuisine_id) VALUES (%s,%s);"
        recipe_creation_cuisines_input = (recipe_id,int(k))
        pymysql_cursor.execute(recipe_creation_cuisines_sql,recipe_creation_cuisines_input)
    
    diet_health_type_list_deletion_sql = "DELETE FROM `diet_health_type_lists` WHERE diet_health_type_lists.recipe_id = %s;"    
    pymysql_cursor.execute(diet_health_type_list_deletion_sql,deletion_recipe_id)
    
    for l in diet_health_types:
        recipe_creation_diet_health_types_sql = "INSERT INTO diet_health_type_lists (recipe_id,diet_health_type_id) VALUES (%s,%s);"
        recipe_creation_diet_health_types_input = (recipe_id,int(l))
        pymysql_cursor.execute(recipe_creation_diet_health_types_sql,recipe_creation_diet_health_types_input)
    
    dish_type_list_deletion_sql = "DELETE FROM `dish_type_lists` WHERE dish_type_lists.recipe_id = %s;"    
    pymysql_cursor.execute(dish_type_list_deletion_sql,deletion_recipe_id)
    
    for m in dish_types:
        recipe_creation_dish_types_sql = "INSERT INTO dish_type_lists (recipe_id,dish_type_id) VALUES (%s,%s);"
        recipe_creation_dish_types_input = (recipe_id,int(m))
        pymysql_cursor.execute(recipe_creation_dish_types_sql,recipe_creation_dish_types_input)
    
    meal_type_list_deletion_sql = "DELETE FROM `meal_type_lists` WHERE meal_type_lists.recipe_id = %s;"    
    pymysql_cursor.execute(meal_type_list_deletion_sql,deletion_recipe_id)
    
    for n in meal_types:
        recipe_creation_meal_types_sql = "INSERT INTO meal_type_lists (recipe_id,meal_type_id) VALUES (%s,%s);"
        recipe_creation_meal_types_input = (recipe_id,int(n))
        pymysql_cursor.execute(recipe_creation_meal_types_sql,recipe_creation_meal_types_input)
    
    pymysql_connection.commit()
    
    return True

def check_if_the_user_is_the_current_posts_author(user_id,recipe_id):
    
    check_sql = "SELECT authors.user_id FROM `authors` JOIN `recipes` ON authors.id = recipes.author_id WHERE recipes.id = %s"
    current_recipe_id = (recipe_id)
    pymysql_cursor.execute(check_sql,current_recipe_id)
    authors_user_id = pymysql_cursor.fetchone()
    
    
    if authors_user_id["user_id"] == user_id:
        return True
    else:
        return False

def delete_post_function(post_id):
    delete_post_recipe_sql = "DELETE FROM `recipes` WHERE recipes.id = %s"
    delete_post_recipe_input = (post_id)
    pymysql_cursor.execute(delete_post_recipe_sql,delete_post_recipe_input)
    return True

def delete_user_function(user_id):
    session.pop('username',None)
    delete_user_sql = "DELETE FROM `users` WHERE users.id = %s"
    delete_user_input = (user_id)
    pymysql_cursor.execute(delete_user_sql,delete_user_input)
    return True
    
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
        check_if_user_exists_sql = "SELECT * FROM users WHERE username = %s"
        check_if_user_exists_input = (username_input)
        pymysql_cursor.execute(check_if_user_exists_sql,check_if_user_exists_input)
        existing_user_check = pymysql_cursor.fetchone()
        if(existing_user_check is None):
            hashed_password = bcrypt.generate_password_hash(password_input).decode('utf-8')
            default_profile_picture = "default-profile-picture.png"
            user_creation_sql = "INSERT INTO users (username,password,email,country_of_origin_id,profile_picture_uri) VALUES (%s,%s,%s,%s,%s)"
            user_creation_input = (username_input,hashed_password,email_input,country_input,default_profile_picture)
            pymysql_cursor.execute(user_creation_sql,user_creation_input)
            pymysql_connection.commit()
            
            session["username"]=username_input
            # SHOULD FLASH THE MESSAGE THAT THE USER HAS BEEN CREATED SUCESSFULLY HERE AND THE LOG THE PERSON OUT INSTEAD OF PLACING ONLY THEIR USERNAME INTO THE SESSION.
            return redirect(url_for('init'))
        else:
            error = True
            
            return render_template("signup.html",error=error)
        
@app.route("/user/recipes",methods=["GET","POST"])
def recipes():
    if session:
        current_user_id = session["user_id"]
        if request.method=="GET":
            user_is_an_author = False
            if check_if_user_is_an_author(current_user_id):
                    user_is_an_author =True
                    
            recipe_creator_form_details = get_recipe_creator_form_details()
            
            search_terms = request.args.get("search")
            if search_terms:
                searched_user_recipe_lists_post_list_details = user_recipe_list_search_function(current_user_id,search_terms)
                return render_template("recipes.html",current_user_id=current_user_id,user_recipe_list=searched_user_recipe_lists_post_list_details,recipe_creator_form_details=recipe_creator_form_details)
            else:
                user_recipe_lists_post_list_details = get_user_recipe_lists_post_list_details(current_user_id)
                return render_template("recipes.html",current_user_id=current_user_id,user_recipe_list=user_recipe_lists_post_list_details,user_is_an_author=user_is_an_author,recipe_creator_form_details=recipe_creator_form_details)
            
        else:
            recipe_picture_uri = "null"
            if request.files:
                recipe_photo = request.files["recipe_photo"]
                if recipe_photo.filename == '':
                    print("no file selected")
                else:
                    f = os.path.join(app.config['RECIPE_PICTURE_UPLOAD_FOLDER'], recipe_photo.filename)
                    recipe_photo.save(f)
                    recipe_picture_uri=str(recipe_photo.filename)
                    
            author_id = check_if_user_is_an_author(current_user_id)
            recipe_title = request.form["recipe_title"]
            prep_time = request.form["prep_time"]
            cook_time = request.form["cook_time"]
            ready_in_time = request.form["ready_in_time"]
            serves_number = request.form["serves_number"]
            recipe_procedure = request.form.getlist("recipe_procedure")
            
            allergens = request.form.getlist("allergens")
            cooking_styles = request.form.getlist("cooking_styles")
            cuisines = request.form.getlist("cuisines")
            diet_health_types = request.form.getlist("diet_health_types")
            dish_types = request.form.getlist("dish_types")
            meal_types = request.form.getlist("meal_types")
            
            creation_result = recipe_creator_big_function(recipe_title,author_id,prep_time,cook_time,ready_in_time,serves_number,recipe_procedure,recipe_picture_uri,allergens,cooking_styles,cuisines,diet_health_types,dish_types,meal_types)
            if creation_result == True:
                return redirect(url_for("recipes"))
            else:
                #FLASH ERROR MESSAGES HERE
                return redirect(url_for("recipes")) #CHANGE THIS LINE
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
            
            no_change_required=False
            password_changed=False
            email_changed=False
            email_input = request.form["email_input"]
            password_input = request.form["password_input"]
            bio_input = request.form["bio_input"]
            user_details_sql="SELECT * FROM users WHERE `id` = %s"
            user_details_input=(current_user_id)
            pymysql_cursor.execute(user_details_sql,user_details_input)
            user_details = pymysql_cursor.fetchone()
            if((email_input==user_details["email"] and password_input==user_details["password"])or(email_input=="" and password_input=="")):
                no_change_required=True
            elif((email_input==user_details["email"] or email_input=="") and password_input!=""):
                password_changed=True
                update_user_details_sql = "UPDATE users SET password=%s, bio=%s WHERE id=%s"
                update_user_details_input=(password_input,bio_input,current_user_id)
                
            else:
                email_changed=True
                update_user_details_sql = "UPDATE users SET email = %s, bio=%s WHERE id=%s"
                update_user_details_input=(email_input,bio_input,current_user_id)
            pymysql_cursor.execute(update_user_details_sql,update_user_details_input)
            
            if request.files:
                uploaded_image = request.files["profile-picture-input"]
                if uploaded_image.filename == '':
                    print("no file selected")
                else:
                    f = os.path.join(app.config['PROFILE_PICTURE_UPLOAD_FOLDER'], uploaded_image.filename)
                    uploaded_image.save(f)
                    profile_picture_uri=str(uploaded_image.filename)
                    update_user_photo_sql = "UPDATE users SET profile_picture_uri = %s WHERE id = %s"
                    update_user_photo_input = (profile_picture_uri,current_user_id)
                    
                    pymysql_cursor.execute(update_user_photo_sql,update_user_photo_input)
            
            pymysql_connection.commit()
            
            return render_template("login.html",no_change_required=no_change_required,password_changed=password_changed,email_changed=email_changed)
    else:
        return redirect(url_for("init"))

@app.route("/recipe_list")
def recipe_list():
    if request.args.get("search"):
        search_terms = request.args.get("search")
        searched_recipe_lists_post_list_details = recipe_list_search_function(search_terms)
        return render_template("recipe_list.html",recipe_list=searched_recipe_lists_post_list_details)
    else:
        recipe_lists_post_list_details = get_recipe_lists_post_list_details()
        return render_template("recipe_list.html",recipe_list=recipe_lists_post_list_details)
    
@app.route("/single/<post_id>")
def post(post_id):
    data = get_post_details(post_id)
    categories = get_post_categories(post_id)
    return render_template("single.html",author_details=data[0],recipe_details=data[1],ingredient_details=data[2],recipe_procedure_list=data[3],recipe_time_details_list=data[4],photo_uri=data[5],allergens=categories[0],cooking_styles=categories[1],cuisines=categories[2],diet_health_types=categories[3],dish_types=categories[4],meal_types=categories[5])

@app.route("/single/<post_id>/editor",methods=["GET","POST"])
def recipe_editor(post_id):
    if session:
        current_user_id = session["user_id"]
        if check_if_the_user_is_the_current_posts_author(current_user_id,post_id) == True:
            if request.method == "GET":
                editor_data = get_recipe_details_for_recipe_editor(post_id)
                print(editor_data)
                return render_template("recipe_editor.html",recipe_details=editor_data["current_post_details"],current_post_categories=editor_data["current_post_categories"],all_available_categories=editor_data["all_available_categories"])
            else:
                recipe_picture_uri = "null"
                change_photo_indicator=False
                if request.files:
                    recipe_photo = request.files["recipe_photo"]
                    if recipe_photo.filename == '':
                        print("no file selected")
                    else:
                        f = os.path.join(app.config['RECIPE_PICTURE_UPLOAD_FOLDER'], recipe_photo.filename)
                        recipe_photo.save(f)
                        recipe_picture_uri=str(recipe_photo.filename)
                        change_photo_indicator = True
                        
                recipe_title = request.form["recipe_title"]
                prep_time = request.form["prep_time"]
                cook_time = request.form["cook_time"]
                ready_in_time = request.form["ready_in_time"]
                serves_number = request.form["serves_number"]
                recipe_procedure = request.form.getlist("recipe_procedure")
                
                allergens = request.form.getlist("allergens")
                cooking_styles = request.form.getlist("cooking_styles")
                cuisines = request.form.getlist("cuisines")
                diet_health_types = request.form.getlist("diet_health_types")
                dish_types = request.form.getlist("dish_types")
                meal_types = request.form.getlist("meal_types")
                
                updater_result = recipe_updater_big_function(recipe_title,prep_time,cook_time,ready_in_time,serves_number,recipe_procedure,recipe_picture_uri,allergens,cooking_styles,cuisines,diet_health_types,dish_types,meal_types,post_id,change_photo_indicator)
                if updater_result == True:
                    return redirect(url_for("recipes"))
                else:
                    #FLASH ERROR MESSAGES HERE
                    return redirect(url_for("init")) #CHANGE THIS LINE
        else:
            #FLASH THE USER IS NOT THE AUTHOR OF RECIPE ERROR HERE
            print("YOU ARE NOT THE AUTHOR")
            return redirect(url_for("init"))
    else:
        print("You are not in session")
        return redirect(url_for("init"))
            
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
                               
@app.route("/testing")
def testing():
    recipe_details = get_recipe_details_for_recipe_editor(2)["current_post_details"][0]
    asd = get_recipe_details_for_recipe_editor(2)["current_post_details"][3]
    print(recipe_details)
    print(asd)
    return redirect(url_for('init'))
    
@app.route("/delete-post/<post_id>")
def delete_post(post_id):
    if(delete_post_function(post_id) is True):
        #FLASH THE MESSAGE OF THE POST IS SUCCESSFULLY DELETED
        return redirect(url_for("recipes"))

@app.route("/delete-user/<user_id>")
def delete_user(user_id):
    if(delete_user_function(user_id) is True):
        #FLASH THE MESSAGE THAT THE USER HAS BEEN DELETED
        return redirect(url_for("init"))    
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
