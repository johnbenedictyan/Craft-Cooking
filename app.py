from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,session,flash,abort
from flask_bcrypt import check_password_hash,Bcrypt,generate_password_hash
from flask_s3 import FlaskS3
from werkzeug.utils import secure_filename
from bson import ObjectId
import pymongo,os,pymysql,random,config,boto3,botocore,tempfile,re,urllib.parse,certifi,babel.dates
from datetime import datetime
import env_var
# only comment the 'import env' out when deploying to heroku
db_url = "mongodb+srv://{}:{}@tgc-ci-project-3-cluster-mllxb.mongodb.net/test?retryWrites=true&w=majority".format(os.environ.get("MONGO_DB_USERNAME"),urllib.parse.quote(os.environ.get("MONGO_DB_PASSWORD")))
ssl_cert = certifi.where()
mongo_connection = pymongo.MongoClient(db_url,ssl=True,ssl_ca_certs=ssl_cert)

pymysql_connection = pymysql.connect(host="remotemysql.com",
                             user = os.environ.get("remotemysql_username"),
                             password = os.environ.get("remotemysql_password"),
                             db = os.environ.get("remotemysql_db_name"))

s3 = FlaskS3()
custom_s3 = boto3.client("s3",aws_access_key_id=os.environ.get("AWS_SECRET_KEY_ID"),aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    s3.init_app(app)
    return app

app = create_app()
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

ALLOWED_FILE_EXTENSIONS = app.config["ALLOWED_FILE_EXTENSIONS"]

def upload_picture_to_s3(file, bucket_name, is_profile_picture, acl="public-read"):
    #if is_profile_picture then the file is a profile picture, otherwise it is a recipe picture
    try:
        if is_profile_picture == True:
            filename = "uploads/profile-pictures/{}".format(file.filename)
        else:
            filename = "uploads/recipe-pictures/{}".format(file.filename)
        custom_s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Upload Failed!", e)
        return e
    return "{}{}".format(app.config["UPLOAD_LOCATION"], filename)

def check_if_file_is_allow(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

def username_special_character_cleaner(username_input):
    regex = re.compile("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    if(regex.search(username_input) == None):
        ErrorFlag = False
    else:
        ErrorFlag = True
        ErrorMessage = "Username has special characters"
    return [ErrorFlag,ErrorMessage]

def check_sign_in_details(username_input,password_input):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    check_sql = "SELECT id,password FROM users WHERE `username` = %s"
    check_input = (username_input)
    pymysql_cursor.execute(check_sql,check_input)
    user_details = pymysql_cursor.fetchone()
    pymysql_cursor.close()
    return user_details

def get_user_recipe_details(current_user_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    recipe_details_sql="SELECT `recipes`.`id`,`recipes`.`name` FROM recipes JOIN authors ON `recipes`.`author_id` = `authors`.`id` WHERE `authors`.`user_id` = %s"
    recipe_details_input = (current_user_id)
    pymysql_cursor.execute(recipe_details_sql,recipe_details_input)
    user_recipe_list=pymysql_cursor.fetchall()
    pymysql_cursor.close()
    return user_recipe_list

def get_user_details(current_user_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    user_details_sql="SELECT users.id,users.username,users.email,users.bio,users.profile_picture_uri,countries.country_name,countries.id,authors.user_to_author_date FROM users JOIN countries ON users.country_of_origin_id = countries.id LEFT JOIN authors ON users.id = authors.user_id WHERE `users`.`id` = %s"
    user_details_input=(current_user_id)
    pymysql_cursor.execute(user_details_sql,user_details_input)
    user_details=pymysql_cursor.fetchone()
    pymysql_cursor.close()
    return return_array

def get_post_categories(post_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
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
    pymysql_cursor.close()
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
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    get_author_details_sql = "SELECT users.username,users.id,users.profile_picture_uri,users.bio FROM `authors` JOIN `recipes` ON recipes.author_id = authors.id JOIN `users` ON authors.user_id = users.id WHERE recipes.id = %s"
    get_author_details_input = (post_id)
    pymysql_cursor.execute(get_author_details_sql,get_author_details_input)
    author_details=pymysql_cursor.fetchone()
    get_recipe_details_sql = "SELECT * FROM `recipes` WHERE recipes.id = %s"
    get_recipe_details_input = (post_id)
    pymysql_cursor.execute(get_recipe_details_sql,get_recipe_details_input)
    recipe_details=pymysql_cursor.fetchone()
    get_photo_lists_sql = "SELECT `uri` FROM `recipe_photos` JOIN `recipes` ON recipe_photos.recipe_id = recipes.id WHERE recipes.id = %s"
    get_photo_lists_input = (post_id)
    pymysql_cursor.execute(get_photo_lists_sql,get_photo_lists_input)
    photo_details=pymysql_cursor.fetchone()
    get_ingredient_list_sql = "SELECT ingredient_id,ingredient_amount,measurement_type,extra_information,ingredients.name AS ingredient_name FROM `ingredient_lists` JOIN `ingredients` ON `ingredient_lists`.ingredient_id = `ingredients`.id WHERE `ingredient_lists`.recipe_id = %s"
    get_ingredient_list_input = (post_id)
    pymysql_cursor.execute(get_ingredient_list_sql,get_ingredient_list_input)
    ingredient_list_details = list(pymysql_cursor.fetchall())
    pymysql_cursor.close()
    recipe_procedure = recipe_details["recipe_procedure"]
    recipe_procedure_list = recipe_procedure.split(".")
    for i in recipe_procedure_list:
        if i == "":
            recipe_procedure_list.remove(i)
        else:
            pass
    recipe_time_details_list = [recipe_details["prep_duration_seconds"],recipe_details["cook_duration_seconds"],recipe_details["ready_in_duration_seconds"]]
    photo_uri = photo_details["uri"]
    for j in recipe_time_details_list:
        recipe_time_details_list[recipe_time_details_list.index(j)] = str(j)+" seconds"
    return [author_details,recipe_details,ingredient_list_details,recipe_procedure_list,recipe_time_details_list,photo_uri]

def get_recipe_details_for_recipe_editor(post_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    #Getting the recipe details
    get_recipe_details_sql = "SELECT recipes.serves,recipes.name,recipes.recipe_procedure FROM `recipes` WHERE recipes.id = %s"
    get_recipe_details_input = (post_id)
    pymysql_cursor.execute(get_recipe_details_sql,get_recipe_details_input)
    recipe_details=pymysql_cursor.fetchone()
    get_recipe_time_details_sql = "SELECT recipes.ready_in_duration_seconds,recipes.prep_duration_seconds,recipes.cook_duration_seconds FROM `recipes` WHERE recipes.id = %s"
    get_recipe_time_details_input = (post_id)
    pymysql_cursor.execute(get_recipe_time_details_sql,get_recipe_time_details_input)
    recipe_time_details=pymysql_cursor.fetchone()
    get_ingredient_list_sql = "SELECT ingredient_id,ingredient_amount,measurement_type,extra_information,ingredients.name AS ingredient_name FROM `ingredient_lists` JOIN `ingredients` ON `ingredient_lists`.ingredient_id = `ingredients`.id WHERE `ingredient_lists`.recipe_id = %s"
    get_ingredient_list_input = (post_id)
    pymysql_cursor.execute(get_ingredient_list_sql,get_ingredient_list_input)
    ingredient_details = list(pymysql_cursor.fetchall())
    get_photo_sql = "SELECT `uri` FROM `recipe_photos` JOIN `recipes` ON recipe_photos.recipe_id = recipes.id WHERE recipes.id = %s"
    get_photo_input = (post_id)
    pymysql_cursor.execute(get_photo_sql,get_photo_input)
    photo_uri=pymysql_cursor.fetchone()
    pymysql_cursor.close()

    recipe_details = helper_function_result[0]
    recipe_time_details = helper_function_result[1]
    ingredient_details = helper_function_result[2]
    photo_uri = helper_function_result[3]

    #Getting the post categories for the recipe editor
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
    pymysql_cursor.close()
    current_post_categories_list = [
        cat_allergen,
        cat_cooking_style,
        cat_cuisine,
        cat_diet_health_type,
        cat_dish_type,
        cat_meal_type
        ]

    #Getting the get recipe creator form details.
    all_allergens_sql = "SELECT id,name FROM allergens"
    pymysql_cursor.execute(all_allergens_sql)
    allergens_form_list = pymysql_cursor.fetchall()
    all_cooking_styles_sql = "SELECT id,name FROM cooking_styles"
    pymysql_cursor.execute(all_cooking_styles_sql)
    cooking_styles_form_list = pymysql_cursor.fetchall()
    all_cuisines_sql = "SELECT id,name FROM cuisines"
    pymysql_cursor.execute(all_cuisines_sql)
    cuisines_form_list = pymysql_cursor.fetchall()
    all_diet_health_types_sql = "SELECT id,name FROM diet_health_types"
    pymysql_cursor.execute(all_diet_health_types_sql)
    diet_health_types_form_list = pymysql_cursor.fetchall()
    all_dish_types_sql = "SELECT id,name FROM dish_types"
    pymysql_cursor.execute(all_dish_types_sql)
    dish_types_form_list = pymysql_cursor.fetchall()
    all_meal_types_sql = "SELECT id,name FROM meal_types"
    pymysql_cursor.execute(all_meal_types_sql)
    meal_types_form_list = pymysql_cursor.fetchall()
    all_ingredient_sql = "SELECT id,name FROM ingredients"
    pymysql_cursor.execute(all_ingredient_sql)
    ingredient_list = pymysql_cursor.fetchall()

    all_categories_list = [allergens_form_list,cooking_styles_form_list,cuisines_form_list,diet_health_types_form_list,dish_types_form_list,meal_types_form_list]
    all_ingredients_list = ingredient_list


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
        "all_available_categories":all_categories_list,
        "all_available_ingredients":all_ingredients_list
    }
    pymysql_cursor.close()
    return result

def recipe_list_helper_function(recipe_lists_post_list_details):
    for i in recipe_lists_post_list_details:
        #Get post categories
        pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
        post_id = int(i['post_id'])
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
        pymysql_cursor.close()
        category_lists_details = [
            allergen_lists_details,
            cooking_style_lists_details,
            cuisine_lists_details,
            diet_health_type_lists_details,
            dish_type_lists_details,
            meal_type_lists_details
            ]
        categories = category_lists_details

        total_number_of_categories = 0
        for j in categories:
            total_number_of_categories += len(j)
        if total_number_of_categories <= 5:
            i["allergens"] = categories[0]
            i["cooking_styles"] = categories[1]
            i["cuisines"] = categories[2]
            i["diet_health_types"] = categories[3]
            i["dish_types"] = categories[4]
            i["meal_types"] = categories[5]
        else:
            i["allergens"] = [
                random.choice(categories[0])
                ]
            i["cooking_styles"] = [
                random.choice(categories[1])
                ]
            i["cuisines"] = [
                random.choice(categories[2])
                ]
            i["diet_health_types"] = [
                random.choice(categories[3])
                ]
            i["dish_types"] = [
                random.choice(categories[4])
                ]
            i["meal_types"] = [
                random.choice(categories[5])
                ]

    return recipe_lists_post_list_details

def get_recipe_lists_post_list_details():
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    recipe_lists_details_sql = """SELECT recipes.name AS post_recipe_name, posts.date_published AS post_date_published, recipe_photos.uri AS post_photo_uri, posts.number_of_views AS post_number_of_views,
    recipes.id AS post_recipe_id, posts.id AS post_id FROM `posts` JOIN `recipes` ON posts.recipe_id = recipes.id JOIN `recipe_photos` ON recipes.id = recipe_photos.recipe_id"""
    pymysql_cursor.execute(recipe_lists_details_sql)
    recipe_lists_post_list_details=pymysql_cursor.fetchall()
    result = recipe_list_helper_function(recipe_lists_post_list_details)
    pymysql_cursor.close()
    return result

def get_user_recipe_lists_post_list_details(current_user_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    recipe_lists_details_sql = """SELECT recipes.name AS post_recipe_name, posts.date_published AS post_date_published, recipe_photos.uri AS post_photo_uri,
    posts.number_of_views AS post_number_of_views,recipes.id AS post_recipe_id, posts.id AS post_id  FROM `posts` JOIN `recipes` ON posts.recipe_id = recipes.id
    JOIN `recipe_photos` ON recipes.id = recipe_photos.recipe_id JOIN `authors` ON recipes.author_id = authors.id WHERE authors.user_id = %s """
    recipe_lists_details_input = (current_user_id)
    pymysql_cursor.execute(recipe_lists_details_sql,recipe_lists_details_input)
    recipe_lists_post_list_details=pymysql_cursor.fetchall()
    result = recipe_list_helper_function(recipe_lists_post_list_details)
    pymysql_cursor.close()
    return result

def recipe_list_search_function(search_terms,categories_only):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
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
    recipe_input_array = [result_2,result_3,result_4,result_5,result_6]
    if categories_only != True:
        pymysql_cursor.execute(sql_1,search_input)
        result_1=pymysql_cursor.fetchall()
        recipe_input_array.insert(0,result_1)

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
    pymysql_cursor.close()
    return result

def user_recipe_list_search_function(current_user_id,search_terms):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
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
    pymysql_cursor.close()
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
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    get_author_id_sql = "SELECT id FROM authors WHERE authors.user_id = %s"
    get_author_id_input = (current_user_id)
    pymysql_cursor.execute(get_author_id_sql,get_author_id_input)
    result = pymysql_cursor.fetchone()
    pymysql_cursor.close()
    if result:
        author_id = int(result["id"])
        return author_id
    else:
        return None

def get_recipe_creator_form_details():
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    all_allergens_sql = "SELECT id,name FROM allergens"
    pymysql_cursor.execute(all_allergens_sql)
    allergens_form_list = pymysql_cursor.fetchall()
    all_cooking_styles_sql = "SELECT id,name FROM cooking_styles"
    pymysql_cursor.execute(all_cooking_styles_sql)
    cooking_styles_form_list = pymysql_cursor.fetchall()
    all_cuisines_sql = "SELECT id,name FROM cuisines"
    pymysql_cursor.execute(all_cuisines_sql)
    cuisines_form_list = pymysql_cursor.fetchall()
    all_diet_health_types_sql = "SELECT id,name FROM diet_health_types"
    pymysql_cursor.execute(all_diet_health_types_sql)
    diet_health_types_form_list = pymysql_cursor.fetchall()
    all_dish_types_sql = "SELECT id,name FROM dish_types"
    pymysql_cursor.execute(all_dish_types_sql)
    dish_types_form_list = pymysql_cursor.fetchall()
    all_meal_types_sql = "SELECT id,name FROM meal_types"
    pymysql_cursor.execute(all_meal_types_sql)
    meal_types_form_list = pymysql_cursor.fetchall()
    all_ingredient_sql = "SELECT id,name FROM ingredients"
    pymysql_cursor.execute(all_ingredient_sql)
    ingredient_list = pymysql_cursor.fetchall()
    pymysql_cursor.close()
    result = [ingredient_list,allergens_form_list,cooking_styles_form_list,cuisines_form_list,diet_health_types_form_list,dish_types_form_list,meal_types_form_list]
    return result

def ingredient_list_packing_function(unpacked_ingredient_list_array):
    result_array = []
    for i in range(len(unpacked_ingredient_list_array[0])):
        result_array.append([unpacked_ingredient_list_array[0][i],unpacked_ingredient_list_array[1][i],unpacked_ingredient_list_array[2][i],unpacked_ingredient_list_array[3][i]])
    return result_array

def recipe_creator_big_function(recipe_title,author_id,prep_time,cook_time,ready_in_time,serves_number,recipe_procedure,recipe_picture_uri,allergens,cooking_styles,cuisines,diet_health_types,dish_types,meal_types,packed_ingredient_array,recipe_description):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    final_recipe_procedure_result = ""
    for i in recipe_procedure:
        if(i[len(i)-1]=="."):
            final_recipe_procedure_result+=i
        else:
            i += "."
            final_recipe_procedure_result+=i
    recipe_creation_sql = "INSERT INTO recipes (id,name,author_id,prep_duration_seconds,cook_duration_seconds,ready_in_duration_seconds,serves,recipe_procedure,description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    recipe_creation_input = (None,recipe_title,author_id,prep_time,cook_time,ready_in_time,serves_number,final_recipe_procedure_result,recipe_description)
    pymysql_cursor.execute(recipe_creation_sql,recipe_creation_input)
    pymysql_connection.commit()
    lastest_recipe_id = int(pymysql_cursor.lastrowid)
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
    for i in cooking_styles:
        recipe_creation_cooking_styles_sql = "INSERT INTO cooking_style_lists (recipe_id,cooking_style_id) VALUES (%s,%s);"
        recipe_creation_cooking_styles_input = (lastest_recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_cooking_styles_sql,recipe_creation_cooking_styles_input)
    for i in cuisines:
        recipe_creation_cuisines_sql = "INSERT INTO cuisine_lists (recipe_id,cuisine_id) VALUES (%s,%s);"
        recipe_creation_cuisines_input = (lastest_recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_cuisines_sql,recipe_creation_cuisines_input)
    for i in diet_health_types:
        recipe_creation_diet_health_types_sql = "INSERT INTO diet_health_type_lists (recipe_id,diet_health_type_id) VALUES (%s,%s);"
        recipe_creation_diet_health_types_input = (lastest_recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_diet_health_types_sql,recipe_creation_diet_health_types_input)
    for i in dish_types:
        recipe_creation_dish_types_sql = "INSERT INTO dish_type_lists (recipe_id,dish_type_id) VALUES (%s,%s);"
        recipe_creation_dish_types_input = (lastest_recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_dish_types_sql,recipe_creation_dish_types_input)
    for i in meal_types:
        recipe_creation_meal_types_sql = "INSERT INTO meal_type_lists (recipe_id,meal_type_id) VALUES (%s,%s);"
        recipe_creation_meal_types_input = (lastest_recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_meal_types_sql,recipe_creation_meal_types_input)
    for i in packed_ingredient_array:
        ingredient_list_sql = "INSERT INTO `ingredient_lists`(`recipe_id`, `ingredient_id`, `ingredient_amount`, `measurement_type`, `extra_information`) VALUES (%s,%s,%s,%s,%s);"
        ingredient_list_input = (lastest_recipe_id,i[0],i[1],i[2],i[3])
        pymysql_cursor.execute(ingredient_list_sql,ingredient_list_input)
    pymysql_connection.commit()
    pymysql_cursor.close()
    return True

def recipe_updater_big_function(recipe_title,prep_time,cook_time,ready_in_time,serves_number,recipe_procedure,recipe_picture_uri,allergens,cooking_styles,cuisines,diet_health_types,dish_types,meal_types,recipe_id,change_photo_indicator,packed_ingredient_array,recipe_description):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    final_recipe_procedure_result = ""
    for i in recipe_procedure:
        if(i[len(i)-1]=="."):
            final_recipe_procedure_result+=i
        else:
            i += "."
            final_recipe_procedure_result+=i
    deletion_recipe_id = (recipe_id)
    recipe_update_sql = "UPDATE recipes SET name=%s,prep_duration_seconds=%s,cook_duration_seconds=%s,ready_in_duration_seconds=%s,serves=%s,recipe_procedure=%s,description=%s WHERE recipes.id=%s;"
    recipe_update_input = (recipe_title,prep_time,cook_time,ready_in_time,serves_number,final_recipe_procedure_result,recipe_description,recipe_id)
    pymysql_cursor.execute(recipe_update_sql,recipe_update_input)
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
    for i in cooking_styles:
        recipe_creation_cooking_styles_sql = "INSERT INTO cooking_style_lists (recipe_id,cooking_style_id) VALUES (%s,%s);"
        recipe_creation_cooking_styles_input = (recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_cooking_styles_sql,recipe_creation_cooking_styles_input)
    cuisine_list_deletion_sql = "DELETE FROM `cuisine_lists` WHERE cuisine_lists.recipe_id = %s;"
    pymysql_cursor.execute(cuisine_list_deletion_sql,deletion_recipe_id)
    for i in cuisines:
        recipe_creation_cuisines_sql = "INSERT INTO cuisine_lists (recipe_id,cuisine_id) VALUES (%s,%s);"
        recipe_creation_cuisines_input = (recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_cuisines_sql,recipe_creation_cuisines_input)
    diet_health_type_list_deletion_sql = "DELETE FROM `diet_health_type_lists` WHERE diet_health_type_lists.recipe_id = %s;"
    pymysql_cursor.execute(diet_health_type_list_deletion_sql,deletion_recipe_id)
    for i in diet_health_types:
        recipe_creation_diet_health_types_sql = "INSERT INTO diet_health_type_lists (recipe_id,diet_health_type_id) VALUES (%s,%s);"
        recipe_creation_diet_health_types_input = (recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_diet_health_types_sql,recipe_creation_diet_health_types_input)
    dish_type_list_deletion_sql = "DELETE FROM `dish_type_lists` WHERE dish_type_lists.recipe_id = %s;"
    pymysql_cursor.execute(dish_type_list_deletion_sql,deletion_recipe_id)
    for i in dish_types:
        recipe_creation_dish_types_sql = "INSERT INTO dish_type_lists (recipe_id,dish_type_id) VALUES (%s,%s);"
        recipe_creation_dish_types_input = (recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_dish_types_sql,recipe_creation_dish_types_input)
    meal_type_list_deletion_sql = "DELETE FROM `meal_type_lists` WHERE meal_type_lists.recipe_id = %s;"
    pymysql_cursor.execute(meal_type_list_deletion_sql,deletion_recipe_id)
    for i in meal_types:
        recipe_creation_meal_types_sql = "INSERT INTO meal_type_lists (recipe_id,meal_type_id) VALUES (%s,%s);"
        recipe_creation_meal_types_input = (recipe_id,int(i))
        pymysql_cursor.execute(recipe_creation_meal_types_sql,recipe_creation_meal_types_input)
    ingredient_list_deletion_sql = "DELETE FROM `ingredient_lists` WHERE `ingredient_lists`.recipe_id = %s"
    pymysql_cursor.execute(ingredient_list_deletion_sql,deletion_recipe_id)
    for i in packed_ingredient_array:
        ingredient_list_sql = "INSERT INTO `ingredient_lists`(`recipe_id`, `ingredient_id`, `ingredient_amount`, `measurement_type`, `extra_information`) VALUES (%s,%s,%s,%s,%s);"
        ingredient_list_input = (recipe_id,i[0],i[1],i[2],i[3])
        pymysql_cursor.execute(ingredient_list_sql,ingredient_list_input)
    pymysql_connection.commit()
    pymysql_cursor.close()
    return True

def category_id_to_category_name(category_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    sql = "SELECT name FROM `categories` WHERE id = %s"
    pymysql_cursor.execute(sql,category_id)
    category_name = pymysql_cursor.fetchone()["name"]
    pymysql_cursor.close()
    return category_name

def check_if_the_user_is_the_current_posts_author(user_id,recipe_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    check_sql = "SELECT authors.user_id FROM `authors` JOIN `recipes` ON authors.id = recipes.author_id WHERE recipes.id = %s"
    current_recipe_id = (recipe_id)
    pymysql_cursor.execute(check_sql,current_recipe_id)
    authors_user_id = pymysql_cursor.fetchone()
    pymysql_cursor.close()
    if authors_user_id["user_id"] == user_id:
        return True
    else:
        return False

def delete_post_function(post_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    delete_post_recipe_sql = "DELETE FROM `recipes` WHERE recipes.id = %s"
    delete_post_recipe_input = (post_id)
    pymysql_cursor.execute(delete_post_recipe_sql,delete_post_recipe_input)
    pymysql_connection.commit()
    pymysql_cursor.close()
    return True

def delete_user_function(user_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    session.pop('username',None)
    delete_user_sql = "DELETE FROM `users` WHERE users.id = %s"
    delete_user_input = (user_id)
    pymysql_cursor.execute(delete_user_sql,delete_user_input)
    pymysql_connection.commit()
    pymysql_cursor.close()
    return True

def user_to_author_function(user_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    user_to_author_sql = "INSERT INTO `authors`(`id`, `user_id`, `user_to_author_date`) VALUES (%s,%s,CURRENT_DATE())"
    user_to_author_input = (None,user_id)
    pymysql_cursor.execute(user_to_author_sql,user_to_author_input)
    pymysql_connection.commit()
    pymysql_cursor.close()
    return True

def get_top_recipe_lists_post_list_details():
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    top_recipe_lists_details_sql = "SELECT recipes.name AS post_recipe_name,recipe_photos.uri AS post_photo_uri,posts.id AS post_id,recipes.description AS post_recipe_description FROM `posts` JOIN `recipes` ON posts.recipe_id = recipes.id JOIN `recipe_photos` ON recipes.id = recipe_photos.recipe_id ORDER BY `posts`.`number_of_views` DESC LIMIT 5"
    pymysql_cursor.execute(top_recipe_lists_details_sql)
    top_recipe_lists_post_list_details=pymysql_cursor.fetchall()
    pymysql_cursor.close()
    return top_recipe_lists_post_list_details

def get_top_categories():
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    top_categories_sql = "SELECT id AS category_id,bg_sm_uri AS category_uri,name AS category_name FROM `categories` ORDER BY `number_of_views` DESC LIMIT 5"
    pymysql_cursor.execute(top_categories_sql)
    top_categories_list=pymysql_cursor.fetchall()
    pymysql_cursor.close()
    return top_categories_list

def categories_view_adder_from_posts_function(post_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    cooking_styles_match_sql = "SELECT categories.id AS category_id FROM posts JOIN recipes ON posts.recipe_id=recipes.id JOIN cooking_style_lists ON recipes.id=cooking_style_lists.recipe_id JOIN cooking_styles ON cooking_style_lists.cooking_style_id=cooking_styles.id JOIN categories ON cooking_styles.name=categories.name WHERE posts.id = %s"
    pymysql_cursor.execute(cooking_styles_match_sql,post_id)
    cat_cs=pymysql_cursor.fetchall()

    diet_health_types_match_sql = "SELECT categories.id AS category_id FROM posts JOIN recipes ON posts.recipe_id=recipes.id JOIN diet_health_type_lists ON recipes.id=diet_health_type_lists.recipe_id JOIN diet_health_types ON diet_health_type_lists.diet_health_type_id=diet_health_types.id JOIN categories ON diet_health_types.name=categories.name WHERE posts.id = %s"
    pymysql_cursor.execute(diet_health_types_match_sql,post_id)
    cat_dht=pymysql_cursor.fetchall()

    dish_types_match_sql = "SELECT categories.id AS category_id FROM posts JOIN recipes ON posts.recipe_id=recipes.id JOIN dish_type_lists ON recipes.id=dish_type_lists.recipe_id JOIN dish_types ON dish_type_lists.dish_type_id=dish_types.id JOIN categories ON dish_types.name=categories.name WHERE posts.id = %s"
    pymysql_cursor.execute(dish_types_match_sql,post_id)
    cat_dtm=pymysql_cursor.fetchall()

    meal_types_match_sql = "SELECT categories.id AS category_id FROM posts JOIN recipes ON posts.recipe_id=recipes.id JOIN meal_type_lists ON recipes.id=meal_type_lists.recipe_id JOIN meal_types ON meal_type_lists.meal_type_id=meal_types.id JOIN categories ON meal_types.name=categories.name WHERE posts.id = %s"
    pymysql_cursor.execute(meal_types_match_sql,post_id)
    cat_mt=pymysql_cursor.fetchall()

    cuisines_match_sql = "SELECT categories.id AS category_id FROM posts JOIN recipes ON posts.recipe_id=recipes.id JOIN cuisine_lists ON recipes.id=cuisine_lists.recipe_id JOIN cuisines ON cuisine_lists.cuisine_id=cuisines.id JOIN categories ON cuisines.name=categories.name WHERE posts.id = %s"
    pymysql_cursor.execute(cuisines_match_sql,post_id)
    cat_c=pymysql_cursor.fetchall()

    def packing_function(input):
        dump_array = []
        for i in input:
            dump_array.append(i["category_id"])
        return dump_array

    cat_array = packing_function(cat_cs) + packing_function(cat_dht) + packing_function(cat_dtm) + packing_function(cat_mt) + packing_function(cat_c)
    categories_view_counter_sql = "SELECT `categories`.`number_of_views` FROM `categories` WHERE id = %s"
    categories_update_counter_sql = "UPDATE `categories` SET `number_of_views`= %s WHERE `categories`.id = %s"
    for i in cat_array:
        pymysql_cursor.execute(categories_view_counter_sql,i)
        number_of_views = int(pymysql_cursor.fetchone()["number_of_views"])
        number_of_views += 1
        categories_update_counter_input = (number_of_views,i)
        pymysql_cursor.execute(categories_update_counter_sql,categories_update_counter_input)
        pymysql_connection.commit()
    pymysql_cursor.close()

def categories_view_adder_function(category_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    categories_view_counter_sql = "SELECT number_of_views FROM `categories` WHERE `categories`.id = %s"
    categories_view_counter_input = (category_id)
    pymysql_cursor.execute(categories_view_counter_sql,categories_view_counter_input)
    number_of_views = int(pymysql_cursor.fetchone()["number_of_views"])
    new_number_of_views = number_of_views + 1
    categories_view_update_sql = "UPDATE `categories` SET `number_of_views`= %s WHERE `categories`.id = %s"
    categories_view_update_input = (new_number_of_views,category_id)
    pymysql_cursor.execute(categories_view_update_sql,categories_view_update_input)
    pymysql_connection.commit()
    pymysql_cursor.close()

def post_view_adder_function(post_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    post_view_counter_sql = "SELECT number_of_views FROM `posts` WHERE `posts`.id = %s"
    post_view_counter_input = (post_id)
    pymysql_cursor.execute(post_view_counter_sql,post_view_counter_input)
    number_of_views = int(pymysql_cursor.fetchone()["number_of_views"])
    number_of_views += 1
    post_view_update_sql = "UPDATE `posts` SET `number_of_views`= %s WHERE `posts`.id = %s"
    post_view_update_input = (number_of_views,post_id)
    pymysql_cursor.execute(post_view_update_sql,post_view_update_input)
    pymysql_connection.commit()
    pymysql_cursor.close()

def check_if_post_exist(post_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    check_if_post_exist_sql = "SELECT recipe_id FROM `posts` WHERE id=%s"
    check_if_post_exist_input = (post_id)
    pymysql_cursor.execute(check_if_post_exist_sql,check_if_post_exist_input)
    post = pymysql_cursor.fetchone()
    pymysql_cursor.close()
    return post

def check_if_user_exist(user_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    check_if_user_exist_sql = "SELECT username FROM `users` WHERE id=%s"
    check_if_user_exist_input = (user_id)
    pymysql_cursor.execute(check_if_user_exist_sql,check_if_user_exist_input)
    username = pymysql_cursor.fetchone()
    pymysql_cursor.close()
    return username

def update_user_profile_photo(profile_picture_uri,current_user_id):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    try:
        update_user_photo_sql = "UPDATE users SET profile_picture_uri = %s WHERE id = %s"
        update_user_photo_input = (profile_picture_uri,current_user_id)
        pymysql_cursor.execute(update_user_photo_sql,update_user_photo_input)
        pymysql_connection.commit()
    except:
        error = "An error has occured in the update_user_profile_photo function."
    finally:
        pymysql_cursor.close()
        return error

def update_user_details(current_user_id,email_input,password_input,bio_input):
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    if password_input == "":
        update_user_details_sql = "UPDATE `users` SET `email`=%s,`bio`=%s WHERE id = %s"
        update_user_details_input=(email_input,bio_input,current_user_id)
    else:
        hashed_password = bcrypt.generate_password_hash(password_input).decode('utf-8')
        update_user_details_sql = "UPDATE `users` SET `password`=%s,`email`=%s,`bio`=%s WHERE id = %s"
        update_user_details_input=(hashed_password,email_input,bio_input,current_user_id)
    try:
        pymysql_cursor.execute(update_user_details_sql,update_user_details_input)
        pymysql_connection.commit()
    except:
        error = "An error has occured in the update_user_details function."
    finally:
        pymysql_cursor.close()
        return error

def get_comments(post_id):
    comments = mongo_connection["tgc-ci-project-3-db"]["comments-collection"]
    comment_query = { "parent_post_id": post_id }
    sort = [('timestamp', -1)]
    comment_list = list(comments.find(comment_query).sort(sort))
    return comment_list

def comment_packaging_function(comment_array):
    result_array = []
    for i in comment_array:
        if i["parent_comment_id"] == None:
            #These are fresh/parent commments.
            dump_dict = {
            "parent": i,
            "children":[]
            }
            result_array.append(dump_dict)
        else:
            #These are children comments.
            for j in result_array:
                if i["parent_comment_id"] == j["_id"]:
                    j["children"].append(i)
    return result_array

def post_comment(current_user_id,parent_object_type,parent_post_id,comment,parent_comment_id=None):
    comments = mongo_connection["tgc-ci-project-3-db"]["comments-collection"]
    if parent_object_type == "post":
        new_comment = {
            "user_id":current_user_id,
            "parent_post_id":parent_post_id,
            "parent_comment_id":parent_comment_id,
            "date_time_created":datetime.utcnow(),
            "comment":comment
        }
    else:
        new_comment = {
            "user_id":current_user_id,
            "parent_post_id":parent_post_id,
            "parent_comment_id":ObjectId(parent_comment_id),
            "date_time_created":datetime.utcnow(),
            "comment":comment
        }
    print(new_comment)
    # inserted_comment = comments.insert_one(new_comment)
    # return inserted_comment.inserted_id

def edit_comment(comment_id,comment):
    comments = mongo_connection["tgc-ci-project-3-db"]["comments-collection"]
    comment_query = { "_id": ObjectId(comment_id) }
    new_comment = { "$set": { "comment": comment } }
    updated_comment = comments.update_one(comment_query, new_comment)
    return updated_comment

@app.template_filter('formatdatetime')
def format_datetime(value, format="medium"):
    """Format a date time to: d Mon YYYY"""
    if value is None:
        return ""
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm"
    return babel.dates.format_datetime(value, format)

@app.route("/")
def init():
    top_recipe_list = get_top_recipe_lists_post_list_details()
    top_categories = get_top_categories()
    return render_template("index.html",session=session,top_recipes=top_recipe_list,recipe_picture_url=app.config['RECIPE_PICTURE_LOCATION'],top_categories=top_categories)

@app.route("/sign_in",methods=["GET","POST"])
def sign_in():
    if request.method == "GET":
        return render_template("sign_in.html")
    else:
        username_input = request.form["username_input"]
        password_input = request.form["password_input"]
        user_details = check_sign_in_details(username_input,password_input)
        if user_details is not None:
            stored_password = user_details["password"]
            if bcrypt.check_password_hash(stored_password,password_input):
                session["username"] = username_input
                session["user_id"] = user_details["id"]
                return redirect(url_for("init"))
            else:
                flash("Incorrect Password", "error")
                return redirect(url_for("sign_in"))
        else:
            flash("This account does not exist", "error")
            return redirect(url_for("sign_in"))

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username',None)
    return redirect(url_for("init"))

@app.route("/sign_up",methods=["GET","POST"])
def user_creation():
    pymysql_cursor = pymysql.cursors.DictCursor(pymysql_connection)
    if request.method == "GET":
        country_sql = "SELECT * FROM `countries`"
        pymysql_cursor.execute(country_sql)
        country_list = pymysql_cursor.fetchall()
        pymysql_cursor.close()
        return render_template("sign_up.html",country_list=country_list)
    else:
        email_input = request.form["email_input"]
        username_input = request.form["username_input"]
        password_input = request.form["password_input"]
        country_input = request.form["country_input"]
        if username_input == None or password_input == None:
            if username_input == None:
                flash("Username is blank","error")
            if password_input == None:
                flash("Password is blank","error")
            return redirect(url_for('user_creation'))
        else:
            if (username_special_character_cleaner(username_input)[0]==False):
                if(check_if_user_exist(username_input) is None):
                    hashed_password = bcrypt.generate_password_hash(password_input).decode('utf-8')
                    default_profile_picture = "default-profile-picture.png"
                    user_creation_sql = "INSERT INTO users (username,password,email,country_of_origin_id,profile_picture_uri) VALUES (%s,%s,%s,%s,%s)"
                    user_creation_input = (username_input,hashed_password,email_input,country_input,default_profile_picture)
                    pymysql_cursor.execute(user_creation_sql,user_creation_input)
                    pymysql_connection.commit()
                    pymysql_cursor.close()
                    flash("Your account has been created!", "message")
                    return redirect(url_for('logout'))
                else:
                    pymysql_cursor.close()
                    flash("This username has been taken!", "error")
                    return redirect(url_for('user_creation'))
            else:
                if(username_special_character_cleaner(username_input)[1]=="Username has special characters"):
                    flash("Invalid Username","error")
                    return redirect(url_for('user_creation'))

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
                return render_template("recipes.html",current_user_id=current_user_id,user_recipe_list=searched_user_recipe_lists_post_list_details,recipe_creator_form_details=recipe_creator_form_details,recipe_picture_url=app.config['RECIPE_PICTURE_LOCATION'])
            else:
                user_recipe_lists_post_list_details = get_user_recipe_lists_post_list_details(current_user_id)
                return render_template("recipes.html",current_user_id=current_user_id,user_recipe_list=user_recipe_lists_post_list_details,user_is_an_author=user_is_an_author,recipe_creator_form_details=recipe_creator_form_details,recipe_picture_url=app.config['RECIPE_PICTURE_LOCATION'])

        else:
            recipe_picture_uri = "null"
            if request.files:
                recipe_photo = request.files["recipe_photo"]
                if recipe_photo.filename == '':
                    flash("A recipe photo is required!", "error")
                    return redirect(url_for("recipes"))
                else:
                    if check_if_file_is_allow(recipe_photo.filename):
                        recipe_photo.filename = secure_filename(recipe_photo.filename)
                        upload_picture_to_s3(recipe_photo, app.config["FLASKS3_BUCKET_NAME"],False)
                        recipe_picture_uri=str(recipe_photo.filename)
                    else:
                        flash("That image extension is not allowed!","error")
                        return redirect(url_for("recipes"))

            author_id = check_if_user_is_an_author(current_user_id)
            recipe_title = request.form["recipe_title"]
            prep_time = request.form["prep_time"]
            cook_time = request.form["cook_time"]
            ready_in_time = request.form["ready_in_time"]
            serves_number = request.form["serves_number"]
            recipe_description = request.form["recipe_description"]
            recipe_procedure = request.form.getlist("recipe_procedure")
            ingredient_list_amount = request.form.getlist("ingredient_list_amount")
            ingredient_list_measurement = request.form.getlist("ingredient_list_measurement")
            ingredient_list_ingredient = request.form.getlist("ingredient_list_ingredient")
            ingredient_list_special = request.form.getlist("ingredient_list_special")
            ingredient_list_array=[ingredient_list_ingredient,ingredient_list_amount,ingredient_list_measurement,ingredient_list_special]
            allergens = request.form.getlist("allergens")
            cooking_styles = request.form.getlist("cooking_styles")
            cuisines = request.form.getlist("cuisines")
            diet_health_types = request.form.getlist("diet_health_types")
            dish_types = request.form.getlist("dish_types")
            meal_types = request.form.getlist("meal_types")

            packed_ingredient_array = ingredient_list_packing_function(ingredient_list_array)
            creation_result = recipe_creator_big_function(recipe_title,author_id,prep_time,cook_time,ready_in_time,serves_number,recipe_procedure,recipe_picture_uri,allergens,cooking_styles,cuisines,diet_health_types,dish_types,meal_types,packed_ingredient_array,recipe_description)
            if creation_result == True:
                flash("The recipe has been successfully created!", "message")
                return redirect(url_for("recipes"))
            else:
                flash("Something went wrong during recipe creation!", "error")
                return redirect(url_for("recipes"))
    else:
        return redirect(url_for("init"))

@app.route("/user",methods=["GET","POST"])
def user_dashboard():
    if session:
        current_user_id = session["user_id"]
        if request.method == "GET":
            user_details = get_user_details(current_user_id)
            user_recipe_list = get_user_recipe_details(current_user_id)
            return render_template("user_dashboard.html",user_details=user_details,user_recipe_list=user_recipe_list,profile_picture_url=app.config['PROFILE_PICTURE_LOCATION'])
        else:
            email_input = request.form["email_input"]
            password_input = request.form["password_input"]
            bio_input = request.form["bio_input"]
            update_user_details(current_user_id,email_input,password_input,bio_input)
            if request.files:
                uploaded_image = request.files["profile-picture-input"]
                if uploaded_image.filename == '':
                    pass
                else:
                    if check_if_file_is_allow(uploaded_image.filename):
                        uploaded_image.filename = secure_filename(uploaded_image.filename)
                        upload_picture_to_s3(uploaded_image, app.config["FLASKS3_BUCKET_NAME"],True)
                        profile_picture_uri=str(uploaded_image.filename)
                        update_user_profile_photo(profile_picture_uri,current_user_id)
                    else:
                        flash("That image extension is not allowed!","error")
                        return redirect(url_for("user_dashboard"))
            flash("Your account details have successfully been updated!","message")
            return redirect(url_for("user_dashboard"))
    else:
        return redirect(url_for("init"))

@app.route("/recipe_list")
def recipe_list():
    if request.args.get("search"):
        search_terms = request.args.get("search")
        searched_recipe_lists_post_list_details = recipe_list_search_function(search_terms,False)
        top_categories = get_top_categories()
        return render_template("recipe_list.html",recipe_list=searched_recipe_lists_post_list_details,recipe_picture_url=app.config['RECIPE_PICTURE_LOCATION'],top_categories=top_categories)
    else:
        recipe_lists_post_list_details = get_recipe_lists_post_list_details()
        top_categories = get_top_categories()
        return render_template("recipe_list.html",recipe_list=recipe_lists_post_list_details,recipe_picture_url=app.config['RECIPE_PICTURE_LOCATION'],top_categories=top_categories)

@app.route("/category/<category_id>")
def single_category(category_id):
    category_name = category_id_to_category_name(category_id)
    searched_recipe_lists_post_list_details = recipe_list_search_function(category_name,True)
    top_categories = get_top_categories()
    return render_template("single_category.html",category_name=category_name,recipe_list=searched_recipe_lists_post_list_details,recipe_picture_url=app.config['RECIPE_PICTURE_LOCATION'],top_categories=top_categories)

@app.route("/single/<int:post_id>",methods=["GET","POST"])
def post(post_id):
    if check_if_post_exist(post_id):
        data = get_post_details(post_id)
        categories = get_post_categories(post_id)
        post_comments = get_comments(post_id)
        post_view_adder_function(post_id)
        if session:
            if request.method=="GET":
                return render_template("single.html",author_details=data[0],recipe_details=data[1],ingredient_details=data[2],recipe_procedure_list=data[3],recipe_time_details_list=data[4],photo_uri=data[5],allergens=categories[0],cooking_styles=categories[1],cuisines=categories[2],diet_health_types=categories[3],dish_types=categories[4],meal_types=categories[5],recipe_picture_url=app.config['RECIPE_PICTURE_LOCATION'],profile_picture_url=app.config['PROFILE_PICTURE_LOCATION'],user_is_sign_in=True,post_comments=post_comments)
            else:
                current_user_id = session["user_id"]
                new_comment = request.form["comment_input"]
                comment_parent_object_type = request.form["parent_obj_type"]
                if comment_parent_object_type == "comment":
                    comment_parent_comment_id = request.form["parent_comment_id"]
                    post_comment(current_user_id,comment_parent_object_type,post_id,new_comment,comment_parent_comment_id)
                else:
                    post_comment(current_user_id,comment_parent_object_type,post_id,new_comment)
                return redirect(url_for("post",post_id=post_id))
        else:
            return render_template("single.html",author_details=data[0],recipe_details=data[1],ingredient_details=data[2],recipe_procedure_list=data[3],recipe_time_details_list=data[4],photo_uri=data[5],allergens=categories[0],cooking_styles=categories[1],cuisines=categories[2],diet_health_types=categories[3],dish_types=categories[4],meal_types=categories[5],recipe_picture_url=app.config['RECIPE_PICTURE_LOCATION'],profile_picture_url=app.config['PROFILE_PICTURE_LOCATION'],post_comments=post_comments)
    else:
        return abort(404)

@app.route("/single/<post_id>/editor",methods=["GET","POST"])
def recipe_editor(post_id):
    if session:
        if check_if_post_exist(post_id):
            current_user_id = session["user_id"]
            if check_if_the_user_is_the_current_posts_author(current_user_id,post_id) == True:
                if request.method == "GET":
                    editor_data = get_recipe_details_for_recipe_editor(post_id)
                    return render_template("recipe_editor.html",recipe_details=editor_data["current_post_details"],current_post_categories=editor_data["current_post_categories"],all_available_categories=editor_data["all_available_categories"],all_available_ingredients=editor_data["all_available_ingredients"])
                else:
                    recipe_picture_uri = "null"
                    change_photo_indicator=False
                    if request.files:
                        recipe_photo = request.files["recipe_photo"]
                        if recipe_photo.filename == '':
                            pass
                        else:
                            if check_if_file_is_allow(recipe_photo.filename):
                                recipe_photo.filename = secure_filename(recipe_photo.filename)
                                upload_picture_to_s3(recipe_photo, app.config["FLASKS3_BUCKET_NAME"],False)
                                recipe_picture_uri=str(recipe_photo.filename)
                                change_photo_indicator = True
                            else:
                                flash("That image extension is not allowed!","error")
                                return redirect(url_for("recipes"))

                    recipe_title = request.form["recipe_title"]
                    prep_time = request.form["prep_time"]
                    cook_time = request.form["cook_time"]
                    ready_in_time = request.form["ready_in_time"]
                    serves_number = request.form["serves_number"]
                    recipe_description = request.form["recipe_description"]
                    recipe_procedure = request.form.getlist("recipe_procedure")
                    allergens = request.form.getlist("allergens")
                    cooking_styles = request.form.getlist("cooking_styles")
                    cuisines = request.form.getlist("cuisines")
                    diet_health_types = request.form.getlist("diet_health_types")
                    dish_types = request.form.getlist("dish_types")
                    meal_types = request.form.getlist("meal_types")
                    ingredient_list_amount = request.form.getlist("ingredient_list_amount")
                    ingredient_list_measurement = request.form.getlist("ingredient_list_measurement")
                    ingredient_list_ingredient = request.form.getlist("ingredient_list_ingredient")
                    ingredient_list_special = request.form.getlist("ingredient_list_special")
                    ingredient_list_array=[ingredient_list_ingredient,ingredient_list_amount,ingredient_list_measurement,ingredient_list_special]
                    packed_ingredient_array = ingredient_list_packing_function(ingredient_list_array)
                    updater_result = recipe_updater_big_function(recipe_title,prep_time,cook_time,ready_in_time,serves_number,recipe_procedure,recipe_picture_uri,allergens,cooking_styles,cuisines,diet_health_types,dish_types,meal_types,post_id,change_photo_indicator,packed_ingredient_array,recipe_description)
                    if updater_result == True:
                        flash("The recipe has been successfully updated!", "message")
                        return redirect(url_for("recipes"))
                    else:
                        flash("Something went wrong during recipe editing!", "error")
                        return redirect(url_for("recipes"))
            else:
                flash("You are not the author of this recipe!", "error")
                return redirect(url_for("recipes"))
        else:
            flash("This recipe does not exist!", "error")
            return redirect(url_for("recipes"))
    else:
        return redirect(url_for("init"))

@app.route("/delete-post/<post_id>")
def delete_post(post_id):
    if session:
        if check_if_post_exist(post_id):
            current_user_id = session["user_id"]
            if check_if_the_user_is_the_current_posts_author(current_user_id,post_id) == True:
                if(delete_post_function(post_id) is True):
                    flash("The recipe has been successfully deleted!", "message")
                    return redirect(url_for("recipes"))
                else:
                    flash("Something went wrong during the deletion process!", "error")
                    return redirect(url_for("recipes"))
            else:
                flash("You are not the author of this recipe!", "error")
                return redirect(url_for("recipes"))
        else:
            flash("This recipe does not exist!", "error")
            return redirect(url_for("recipes"))
    else:
        return redirect(url_for("init"))

@app.route("/delete-user/<user_id>")
def delete_user(user_id):
    if check_if_user_exist(user_id):
        if(delete_user_function(user_id) is True):
            flash("The account has been successfully deleted!", "message")
            return redirect(url_for("init"))
        else:
            flash("Something went wrong!", "message")
            return redirect(url_for("init"))
    else:
        flash("This user does not exist!", "error")
        return redirect(url_for("init"))

@app.route("/become-an-author/<user_id>")
def become_an_author(user_id):
    if check_if_user_exist(user_id):
        if user_to_author_function(user_id) is True:
            flash("You are now an author!", "message")
            return redirect(url_for("user_dashboard"))
        else:
            flash("Something went wrong!", "message")
            return redirect(url_for("init"))
    else:
        flash("This user does not exist!", "error")
        return redirect(url_for("init"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route('/test')
def testinggetcommens():
    get_comments(1)
    categories_view_adder_from_posts_function(1)
    return redirect(url_for('init'))

@app.route("/testingpage")
def testing():
    current_user_id = session["user_id"]
    parent_object = "post"
    parent_post_id = 1
    parent_object_id=None
    comment="This recipe is good."
    post_comment(current_user_id,parent_object,parent_object_id,parent_post_id,comment)
    return redirect(url_for('init'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)
