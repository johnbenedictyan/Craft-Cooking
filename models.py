from flask_sqlalchemy import SQLAlchemy
from app import sql_alchemy_db as db
from datetime import datetime

def view_count_adder(context):
    return context.get_current_parameters()['number_of_views'] + 1

class Users(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    profile_picture_uri = db.Column(db.String, nullable=False, default="default-profile-picture.jpg")
    country_of_origin_id = db.Column(db.Integer(11),db.ForeignKey('Countries.id'))
    country_of_origin = relationship("Countries", back_populates="user")
    recipe = relationship("Recipes", back_populates="user")
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

class Countries(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    user = relationship("Users", back_populates="country_of_origin")

class Posts(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    date_published = db.Column(db.DateTime,default=datetime.date.now)
    number_of_views = db.Column(db.Integer(11),default=view_count_adder,onupdate=view_count_adder)
    recipe_id = db.Column(db.Integer(11),db.ForeignKey('Recipes.id'))
    recipe = relationship("Recipes", back_populates="post")
    last_visited = db.Column(db.DateTime,default=datetime.datetime.now)

    def get_todays_date(self):
        return datetime.datetime.utcnow()

    def last_visited_updated(self):
        self.last_visited = self.get_todays_date()

class Recipes(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    prep_duration_seconds = db.Column(db.Integer(11), nullable=False)
    cook_duration_seconds = db.Column(db.Integer(11), nullable=False)
    ready_in_duration_seconds = db.Column(db.Integer(11), nullable=False)
    serves = db.Column(db.Integer(11), nullable=False)
    recipe_procedure = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text,nullable=True)
    user_id = db.Column(db.Integer(11),db.ForeignKey('Users.id'))
    user = relationship("Users", back_populates="recipe")
    allergen = relationship("Allergens",secondary=allergen_association_table,backref="recipe")
    cooking_style = relationship("Cooking_styles",secondary=cooking_style_association_table,backref="recipe")
    cuisine = relationship("Cuisines",secondary=cuisine_association_table,backref="recipe")
    diet_health_type = relationship("Diet_health_types",secondary=diet_health_type_association_table,backref="recipe")
    dish_type = relationship("Dish_types",secondary=dish_type_association_table,backref="recipe")
    ingredient = relationship("Ingredient_lists",secondary=ingredient_list_association_table,backref="recipe")
    meal_type = relationship("Meal_types",secondary=meal_type_association_table,backref="recipe")

class Categories(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number_of_views = db.Column(db.Integer(11),default=view_count_adder,onupdate=view_count_adder)
    last_visited = db.Column(db.DateTime,default=datetime.datetime.now)

    def get_todays_date(self):
        return datetime.datetime.utcnow()

    def last_visited_updated(self):
        self.last_visited = self.get_todays_date()

class Allergens(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

allergen_association_table = db.Table('allergen_association', db.Model.metadata,
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipes.id')),
    db.Column('allergen_id', db.Integer, db.ForeignKey('Allergens.id'))
)

class Cooking_styles(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

cooking_styles_association_table = db.Table('cooking_styles_association', db.Model.metadata,
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipes.id')),
    db.Column('cooking_style_id', db.Integer, db.ForeignKey('Cooking_styles.id'))
)

class Cuisines(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

cuisine_association_table = db.Table('cuisine_association', db.Model.metadata,
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipes.id')),
    db.Column('cuisine_id', db.Integer, db.ForeignKey('Cuisines.id'))
)

class Diet_health_types(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

diet_health_type_association_table = db.Table('diet_health_type_association', db.Model.metadata,
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipes.id')),
    db.Column('diet_health_type_id', db.Integer, db.ForeignKey('Diet_health_types.id'))
)

class Dish_types(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

dish_type_association_table = db.Table('dish_type_association', db.Model.metadata,
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipes.id')),
    db.Column('dish_type_id', db.Integer, db.ForeignKey('Dish_types.id'))
)

class Ingredients(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredient_list = relationship("Ingredient_lists", back_populates="ingredient")

ingredient_list_association_table = db.Table('ingredient_list_association', db.Model.metadata,
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipes.id')),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('Ingredients.id')),
    db.Column('ingredient_amount',db.String(50), nullable=False),
    db.Column('measurement_type',db.String(50), nullable=False),
    db.Column('extra_information',db.String(50), nullable=False)
)

class Meal_types(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

meal_type_association_table = db.Table('meal_type_association', db.Model.metadata,
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipes.id')),
    db.Column('meal_type_id', db.Integer, db.ForeignKey('Meal_types.id'))
)
