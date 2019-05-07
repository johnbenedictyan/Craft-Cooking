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

Things to note:
1. Use the class "tag-cloud-link" for the categories
2. 

Things needed to be done:
RED:
1. Recipe list search functionality
2. Recipe creator
3. Recipe updator
4. Add in recipes and populate both the front page as well as the recipe list page.
5. When adding to the database, the program should check whether the things already exist in the database.
6. The program should also pass everything into lowercase and singular.
7. Before rendering the single article template. Use a select sql that joins the recipe,author,user to get the author's name. recipe and ingredient list, to get the ingredients. 
    All of the meal type, diet and health,dish type ,cooking style and categories join individually with the recipe and pass the data through so they can be used in the tag-cloud-link thing.
    Join the photos to the recipe to get the uri.
8. Read function for the user dashboard. Change the update profile form to the same layout as the profile.
YELLOW:
1. Form validation so that the users cannot send empty form, preferably cilent side form validation. Also bann the use of unique characters in password to prevent sql injects.
2. Add a bio section to the user and pass into the sql query for author_details.
3. Change the seconds into seconds and minutes in each articles.
4. Change the url for the user profile picture in the user dashboard to a uri that is gotten from a sql search.
GREEN:
1. Reformat the sql select executors into python functions.

Stock profile pictures:
https://www.pexels.com/photo/adult-beard-boy-casual-220453/
https://www.pexels.com/photo/man-in-crew-neck-shirt-555790/
https://www.pexels.com/photo/woman-taking-selfie-while-smiling-1310522/
https://www.pexels.com/photo/smiling-man-in-front-of-green-plants-2078265/
https://www.pexels.com/photo/man-wearing-black-zip-up-hooded-jacket-facing-camera-1080213/

4 May:
Added in the template for single articles.
Added the hero wrap for all of the current pages.
Added the recipe list page.
Added the 404 page.
Added in two dummy articles for the front page.

6 May:
Read function for single article page

7 May:
Profile layout
Profile update layout
