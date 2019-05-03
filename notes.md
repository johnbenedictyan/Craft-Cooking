{{ url_for('static', filename='')}}
background-image: url({{ url_for('static', filename='') }})

Things to check how to do:
1. How to check if select statement returns null 

Things That need to implement:
1. Login in page, check if the password is correct/username exists.
2. Change the navigation page when the person is logged in
3. Recipe editor
4. Find out how to redirect while passing in variables after form post such as login and update user information.
5. Find out how to implement sessions.
6. Need to hash the passwords that they enter
7. Message flashing: http://flask.pocoo.org/docs/1.0/patterns/flashing/
8. Flask bcrypt: https://flask-bcrypt.readthedocs.io/en/latest/
9. Flask sessions: https://www.tutorialspoint.com/flask/flask_sessions.htm || https://pythonhosted.org/Flask-Session/

Session:
app.sercet_key = os.urandom(24)

if 'user' in sessions
session.pop('user',None)