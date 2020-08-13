#Import packages
from flask import Blueprint, request,jsonify
from new import db,user_schema,users_schema,app
from new import Users
import re
from passlib.hash import sha256_crypt

#create a blueprint
users = Blueprint("users",__name__)

#Route for Registering users
@users.route('/users/register', methods=['POST','GET'])
def create_account():

  if request.method == 'POST':
   firstname = request.json['firstname']
   lastname = request.json['lastname']
   email = request.json['email']
   password = request.json['password']

   #secure_password = sha256_crypt.encrypt(str(password)) (optional)

#Filter the data that have specified email
   emaildata = Users.query.filter(Users.email == email)
   final_result = users_schema.dump(emaildata)
#If there is no specified email then final_result will be empty means the user doesn't exist
   if final_result == []:
       new_user = Users(firstname, lastname, email,password)
       db.session.add(new_user)
       db.session.commit()
       return user_schema.jsonify(new_user)
   else:
       return {"message" : "email already exists, please register new email"}

#route for login for users
@users.route('/users/login', methods=['POST','GET'])
def login():

  if request.method == 'POST':
   email = request.json['email']
   password = request.json['password']
#filter out the data that have specified email and password
   email_data = Users.query.filter(Users.email == email).first()
   passwordd = Users.query.filter(Users.password == password).first()

#If no user exists with that email then empty email_data
   if not email_data:
       return {"message":"the user doesn't exist"}
#Apply regular expressions for email if email exists
   elif not re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", email):
       return ("Please enter correct Email Address")
#if correct email exists then check password if it exists for the same user
   elif not passwordd:
       return {"message" : "Please add correct password"}
#Apply regular expressions for password if password exists
   elif not re.match('^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&-+=()])(?=\\S+$).{8, 20}$', password):
       return {"message":"Password must contain more than 8 characters, an uppercase letter, a special character and a digit"}
#If user's Id matches for both password and email i.e <User 1> == <User 1>, then let them login
   elif email_data == passwordd:
       return {"message" : "You have logged In"}
   else:
       return{"message" : "Incorrect Credentials"}

# Run Server
if __name__ == '__main__':
    app.run(debug=True)






