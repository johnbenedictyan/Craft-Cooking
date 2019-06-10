# Things to note:
1. Use the class "tag-cloud-link" for the categories
2. The cuisine, cooking styles,diet and health,dish type, cooking style should all be drop down with the option to add custom values, but the custom values must be approved by an admin figure.
3. The program should pass the inputs into lowercase and singular form for the ingredients
4. Hero images should be at max 2000X2000 ish and recipe thumbnail images should be 1000X1000 ish and their main image can be 2000X2000 ish

# Things needed to be done:

## Code Red
- Single page for all of the categories with a description of each of them and then a recipe_list with a preset search term.
- Find out how to implement website testing

## Code Yellow
 - Form validation so that the users cannot send empty form, preferably the form validation should be on the client side. Also ban the use of unique characters in password to prevent SQL injects.
 - Change the seconds into seconds and minutes in each articles.
 - Add in more recipes into the database and populate the front page


## Code Green
 - Change the upload folder to an external server ssh thingy thingy.
 - The user dashboard navigation should be at the top for mobile devices and tablets.


## Things that don't work
 1. URL_FOR to a folder that is not the static folder. [FIXED][look at 2 on funny things]
 2. Recipe Creator sql doesn't want me to define variables inside of the sql query.


## Things to think about

 1. Get a featured post list where a sql query is set to return a list of the top 5 highest viewed recipes. Put those on the main page.
 2. What is the relationship between users and reviews and recipes. One to many or many to many.


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

## 22 May
- New Feature: Recipe Deletion
- Bug Fix: The bug whereby the user would not be popped out of session when he created a new user whilst being logged in to the old user account.
- New Feature: User Deletion
- Bug Fix: Recipe Procedure buttons not working.
- Formatting: Made all of the recipe photos the same height and limited the number of categories to be displayed to five.

## 23 May
- New Feature: Message Flashing
- Bug Fix: The bug where the updated password wasn't being hashed.
- New Feature: Recipe Creator and Editor now have access to the ingredient list.
- Bug Fix: Added checks to see if users would enter fake user_id and post_id into the urls and placed errors for them.

## 24 May
- New Feature: Each recipe has its own description.
- New Feature: Top five post in terms of number of view show up as the feature posts. Added a function to auto increment the number of views when a post is visited.

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

**Example Modal Box**
- https://www.tutorialrepublic.com/codelab.php?topic=bootstrap&file=delete-confirmation-modal

## Funny things that happened along the way
1. The error of my hashed passwords not matching might be due to the fact that i have limited the amount of characters on the
password in the database to VARCHAR(30). Therefore the stored value would be a truncated version of the hashed password,
therefore the checkpasswordhash function would not work.
2. Fixed the user profile picture delivery system with a custom function which returns a send from directory of the picture.
3. Jquery onclick only works for static buttons whereas the on function works for dynamically added buttons. Thats how i solved the bug of the recipe procedure not working.
4. To make all of the recipes in the recipe list to be of the same height. If the number of categories was above 5, i would randomly choose one from each type of category to display. This however did not affect the search functionality.
5. Select picker wasn't showing up when I added them dynamically, add the selectpicker refresh function to run each time they were added and then it worked.
