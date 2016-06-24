""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

class LoginModel(Model):
    def __init__(self):
        super(LoginModel, self).__init__()
    
    def create_user(self, info):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        first = info['first']
        last = info['last']
        email = info['email']
        password = info['password']
        confirmed = info['confirm']
        valid = True
        errors = []
        if len(first) < 2:
            errors.append("First name too short!")
            valid = False;
        if not first.isalpha():
            errors.append("First name has non letter characters!")
            valid = False;
        if (len(last) < 2):
            flash("Last name too short!")
            valid = False;
        if not last.isalpha():
            errors.append("Last name has non letter characters!")
            valid = False;
        if email < 1:
            errors.append("No email!")
            valid = False;
        if not EMAIL_REGEX.match(email):
            errors.append("Invalid email!")
            valid = False;
        if password < 8:
            errors.append("Password too short!")
            valid = False;
        if password != confirmed:
            errors.append("Passwords do not match!")
            valid = False;
        if valid:
            pw_hash = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users (email, first_name, last_name, pw_hash, created_at, updated_at) " \
                    "VALUES (:email, :first_name, :last_name, :pw_hash, NOW(), NOW())"
            data = {
                'email': email,
                'first_name': first,
                'last_name': last,
                'pw_hash': pw_hash
            }
            self.db.query_db(query, data)
            query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(query)
            return {'valid': True, 'user': users[0]}
        else:
            return {'valid': False, 'errors': errors}

    def login_user(self, info):
        try:
            query = "SELECT * FROM users WHERE email = :email"
            user = self.db.query_db(query, info)
            pw_hash = user[0]['pw_hash']
            errors = []
            if self.bcrypt.check_password_hash(pw_hash, info['password']):
                return{'valid': True, 'user': user[0]}
            else:
                errors.append("Email and password do not match!")
                return {'valid': False, 'errors': errors}
        except IndexError:
            errors.append("Email not in database!")
            return {'valid': False, 'errors': errors}







