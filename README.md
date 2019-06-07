# Craft Cooking
Craft Cooking is a Foodie's Dream. With delicious recipes available for all as well as options to add your very own, there is something for everyone. 
Think you could be the next Jamie Oliver? You have to let the world know of your amazing culinary creations, and you can do so at Craft Cooking!
Craft Cooking is an amazing place to learn about new recipes to spice up your meals. Choose from a variety of cuisines, cooking styles and diet types.
## UX
List of User Stories
- As an aspiring food blogger, I want to publish a recipe, so that I can gather attention to recipes and amass a following.
- As an office worker with little time, I want to know about recipes that can be done under 1 hour, so I can make a fast meal.
- As a vegan, I want to learn about vegan recipes, so that I can stick to my diet.
- AS someone who wants to lose weight, I want to learn about healthy recipes.
- As a chef, I want to review recipes, so that I can help the culinary community grow in their compentency.


## Features
### Existing Features
- Recipe Creation - Allows users to create their own recipes, by having them fill up a recipe creation form.
- Recipe Updating - Allows users to update their own recipes, by having them fill up a recipe update form.
- Recipe Deletion - Allows users to delete their own recipes, with checks in place if they try to delete a recipe they did not create.
- Searching for Recipes - Allows users to search for recipes, by having them type in a search bar.
- User Creation - Allows users to create user accounts, by having them fill up a user creation form.
- User Account Details Updating - Allows users to update their user details, by having them fill up a user details updating form.
- User Deletion - Allows users to create their own recipes, by having them fill up a recipe creation form.
- View Counter - Allows the number of views on each recipe to increase whenever a user clicks on that recipe
- User & Recipe Photo Upload - Allows the user to upload photos for their recipes as well as their profiles, by storing the photos in AWS S3.

### Features Left to Implement
- Comments Section: Where users can leave comments on each of the recipes as well as other's users' comments.
- Review Section: Community driven review section, based of 5 stars, with the inclusion of certified reviewers whose reviews will be highlighted
- Blog Section: Community Written Blogs
- A webpage for each individual category with the relevant recipes displayed

## Technologies Used
- [Boostrap](https://getbootstrap.com/)
    - The project uses **Boostrap** to create a mobile responsive and stylish webpage.
- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.
- [Flask](http://flask.pocoo.org/)
    - The project uses **Flask** as it's main framework.
- [Flask-Bcrypt](https://github.com/maxcountryman/flask-bcrypt)
    - The project uses **Flask-Bcrypt** to hash user passwords.
- [Flask-S3](https://flask-s3.readthedocs.io/en/latest/)
    - The project uses **Flask-S3** to allow for the uploading of photos to AWS S3.
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
    - The project uses **boto3** to allow for the uploading of photos to AWS S3.
- [botocore](https://pypi.org/project/botocore/)
    - The project uses **botocore** to allow for the uploading of photos to AWS S3.
- [cffi](https://pypi.org/project/cffi/)
    - The project uses **cffi** to allow python to call C code.
- [dnspython](https://pypi.org/project/dnspython/)
    - The project uses **dnspython** to allow for the pymongo connection to be more secure.
- [gunicorn](https://gunicorn.org/)
    - The project uses **gunicorn** as a python WSGI HTTP server to deploy the app on Heroku.
- [pymongo](https://api.mongodb.com/python/current/)
    - The project uses **pymongo** to connect the app to a MongoDB Atlas database.
- [PyMySQL](https://github.com/PyMySQL/PyMySQL)
    - The project uses **PyMySQL** to connect the app to a remotemysql database.
- [python-dateutil](https://pypi.org/project/python-dateutil/)
    - The project uses **python-dateutil** to allow python to get the current date.
- [s3transfer](https://pypi.org/project/python-dateutil/)
    - The project uses **s3transfer** to allow for the uploading of photos to AWS S3.
- [urllib3](https://urllib3.readthedocs.io/en/latest/)
    - The project uses **urllib3** as a HTTP client.
- [Boostrap-Select](https://developer.snapappointments.com/bootstrap-select/)
    - The project uses **Boostrap-Select** to allow for the user to search of an option in the select input.
- [Axios](https://github.com/axios/axios/)
    - The project uses **Axios** to simplify AJAX calls.

## Testing
Manual Testing:

Interesting Bugs/Problems:
- The hashed passwords were not being accepted by Flask-Bcrypt as I had limited the number of characters in the password field on the database to only 30. This meant that the stored values were a substring of the actual hashed password and thus would not be accepted by the hashing algorithm.
- Jquery's onclick function would not work for dynamically loaded buttons, therefore I had to switch the Jquery to be an on function instead.
- To make all of the recipes in the recipe list be of the same height. The number of categories displayed for each recipe could not be more than 5. So if the number of categories for a particular recipe was above 5, the app would randomly choose 5 to display. This however does not limit the search functionality.
- The custom selectpicker were not appearing when they were added dynamically, therefore i added a selectpicker refresh function to run each time they were added.

## Deployment
On the development version, sensitive information is stored in an env.py that is not pushed to github.
Where as on the deployed version, these sensitive information are stored in the Heroku Config Vars

To run the app locally:
1. Open the app.py in the main directory.
2. Run this python script.
3. Click on the local host link address to open the app the web browser.

You can view the deployed version on [Heroku](https://tgc-ci-project-3.herokuapp.com/)
## Credits

### Content
- The text for recipes were taken from [Tasty](https://tasty.co/)

### Media
- The photos used in this site were obtained from [Stock Snap](https://stocksnap.io/),[Pexels](https://www.pexels.com/),[Unsplash](https://unsplash.com/),[Pixabay](https://pixabay.com/),[FoodiesFeed](https://www.foodiesfeed.com/)

### Acknowledgements

- The Boostrap Template was taken from [ColorLib](https://colorlib.com/wp/templates/)

