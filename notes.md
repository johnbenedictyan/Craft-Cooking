{{ url_for('static', filename='')}}
background-image: url({{ url_for('static', filename='') }})

Things to check how to do:
1. How to check if select statement returns null 

Things That need to implement:
3. Recipe editor
4. Find out how to redirect while passing in variables after form post such as login and update user information.
7. Message flashing: http://flask.pocoo.org/docs/1.0/patterns/flashing/
8. Flask bcrypt: https://flask-bcrypt.readthedocs.io/en/latest/
9. Flask sessions: https://www.tutorialspoint.com/flask/flask_sessions.htm || https://pythonhosted.org/Flask-Session/

Session:
app.sercet_key = os.urandom(24)

if 'user' in sessions
session.pop('user',None)

the error of my hashed passwords not matching might be due to the fact that i have limited the amount of characters on the 
password in the database to VARCHAR(30). Therefore the stored value would be a truncated version of the hashed password,
therefore the checkpasswordhash function would not work.

{{url_for('FUNCTION NAME')}}

Things needed to be done:
RED:
1. Recipe list search functionality
2. Recipe creator
3. Recipe updator
4. Create an entity for the strawberry pancake(https://www.justsotasty.com/strawberry-pancakes/) and the garlic steak(https://tasty.co/recipe/garlic-butter-steak).
5. Add in recipes and populate both the front page as well as the recipe list page.
YELLOW:
1. Form validation so that the users cannot send empty form, preferably cilent side form validation. Also bann the use of unique characters in password to prevent sql injects.
GREEN:
1. Reformat the sql select executors into python functions.

4 May:
Added in the template for single articles.
Added the hero wrap for all of the current pages.
Added the recipe list page.
Added the 404 page.
Added in two dummy articles for the front page.