# Things to note:
1. Use the class "tag-cloud-link" for the categories
2. The cuisine, cooking styles,diet and health,dish type, cooking style should all be drop down with the option to add custom values, but the custom values must be approved by an admin figure.
3. The program should pass the inputs into lowercase and singular form for the ingredients
4. Hero images should be at max 2000X2000 ish and recipe thumbnail images should be 1000X1000 ish and their main image can be 2000X2000 ish

# Things needed to be done:

## Code Red
- Recipe creator(DONE HALF OF IT, JUST INSERT THE POST CATEGORIES INTO THE DATABASE AND IT SHOULD WORK. CHANGE THE FORM SO THAT A DROPOUT MULTI SELECT CAN BE USED TO SELECT THE CATEGORIES) [DONE]
- Change all the sql statements so that instead of only looking through the categories table(NEED TO GET RID OF THIS GENERIC CATEGORIES TABLE), the <category_link_details> 
will have all of the possible categories from all of the tables (allergens,cookingstyle,health and diet,etc) [UPDATE:CHANGE THE SQL STATEMENTS SO THAT category_link_details is now an array of all of the different categories, 
still need to fix the functions that take that array in) [DONE] 
- Recipe updater
- Add in more recipes into the database and populate the front page
- Before rendering the single page article template. Pass in all of the categories into tag-cloud-links and place them at the bottom of the page [DONE]
- Update the SQL statement so that the meal type, diet and health,dish type ,cooking style show up in the links in each recipe when displayed in the recipe list section. The number of tags should be limited to 5.
- Fix the profile picture uploading [DONE]
- Update the search functionality to also check if the search term matches the cuisine/ingredient rather than just the name of the recipe [DONE]

## Code Yellow

 - Form validation so that the users cannot send empty form, preferably the form validation should be on the client side. Also ban the use of unique characters in password to prevent SQL injects.
 - Add a bio section to the user and pass into the SQL query for author_details. [DONE]
 - Change the seconds into seconds and minutes in each articles.
 - Change the update user details from simple flashing to flask flashing.

## Code Green

 - Change all the '{}'.format() to python prepared statements, to prevent SQL injects.
 - Change the upload folder to an external server ssh thingy thingy.


## Things that don't work
 1. URL_FOR to a folder that is not the static folder. [FIXED][look at 2 on funny things]
 2. Recipe Creator sql doesn't want me to define variables inside of the sql query.


## Things to think about

 1. Decide on whether to use text area or the button which adds a new step for the recipe procedure
 2. Get a featured post list where a sql query is set to return a list of the top 5 highest viewed recipes. Put those on the main page.

# PROJECT LOGS:
## 4 May:
- Added in the template for single articles.
- Added the hero wrap for all of the current pages.
- Added the recipe list page.
- Added the 404 page.
- Added in two dummy articles for the front page.

## 6 May
- Read function for single article page

## 7 May
- Profile layout
- Profile update layout

## 13 May
- Added in the photo to each single article
- Added the function to get all the recipes in the recipe list to show up
- Added in the search function for the recipe lists

## 14 May
- Added in the recipes and the recipe search functionality to each of the user's dashboard
- Added a error handler for when the user reloads the page and the session does not exist but the user is trying to access a page which requires the session to exist.
- Added in all of the countries into the countries table.

## 16 May
- Fixed the profile picture updater and bio updater.
- User Sign ups now can enter their country.

## 19 May
- New Feature: Recipe Creator
- Added in all the categories

## USEFUL LINKS
**Stock profile pictures**
- https://www.pexels.com/photo/adult-beard-boy-casual-220453/
- https://www.pexels.com/photo/man-in-crew-neck-shirt-555790/
- https://www.pexels.com/photo/woman-taking-selfie-while-smiling-1310522/
- https://www.pexels.com/photo/smiling-man-in-front-of-green-plants-2078265/
- https://www.pexels.com/photo/man-wearing-black-zip-up-hooded-jacket-facing-camera-1080213/

**Flask File Uploads**
- http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
- https://pythonhosted.org/Flask-Uploads/
- https://medium.com/@sightengine_/image-upload-and-moderation-with-python-and-flask-e7585f43828a

**Flask Message Flashing**
- https://flask.pocoo.org/docs/1.0/patterns/flashing/

**How to prevent SQL Inject**
- https://tableplus.io/blog/2018/08/best-practices-to-prevent-sql-injection-attacks.html
- https://blog.sqreen.com/preventing-sql-injections-in-python/
- https://damyanon.net/post/flask-series-security/
- http://flask.pocoo.org/docs/1.0/security/

## Funny things that happened along the way
1. The error of my hashed passwords not matching might be due to the fact that i have limited the amount of characters on the 
password in the database to VARCHAR(30). Therefore the stored value would be a truncated version of the hashed password,
therefore the checkpasswordhash function would not work.
2. Fixed the user profile picture delivery system with a custom function which returns a send from directory of the picture.