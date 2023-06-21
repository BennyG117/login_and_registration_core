from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    DB = 'login_and_registration_core'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



        #! Staticmethods here
    #staticmethod to validate email -- is this uneccessary?
    @staticmethod
    def validate_email(new_email):
        is_valid = True
        # test whether email submitted is an actual email
        if not EMAIL_REGEX.match(new_email['email']): 
            flash ("Email is not valid!")
            is_valid = False
        # test to verify the email doesn't already exist in the db
        query = """
        SELECT * 
        FROM users
        WHERE email = %(email)s;
        """    
        results = connectToMySQL('login_and_registration_core').query_db(query,new_email)
        # use to check if working...
        print(results)

        if results:
            flash("Email already exists!")
            is_valid = False

        return is_valid


    #static method to validate entire user (specific to register form)
    @staticmethod
    def validate_user(new_user):
        is_valid = True
        if len(new_user['first_name']) < 2:
            flash('User first name must be 2 charecters or more!', 'register')
            is_valid = False
        if len(new_user['last_name']) < 2:
            flash('User first name must be 2 charecters or more!', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(new_user['email']):
            flash('Please enter a valid email!', 'register')
            is_valid = False
        if len(new_user['password']) < 8:
            flash('Password must be 8 or more characters long!', 'register')
            is_valid = False
        if new_user['password'] != new_user['confirm_password']:
            flash('Passwords did not match!', 'register')
            is_valid = False
        
        return is_valid


        #! Classmethods here

    #classmethod to save new user registration
    @classmethod
    def save(cls,data):
        query = """INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""

        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    #classmethod to get one user (via id)
    @classmethod
    def get_oneById(cls,data):
        query = """
        SELECT * 
        FROM users
        WHERE id = %(id)s;
        """    

        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])


    #classmethod to get one user (via email)
    @classmethod
    def get_oneByEmail(cls,data):
        query = """
        SELECT * 
        FROM users
        WHERE email = %(email)s;
        """    
        #if it's not in the DB it will be False
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])



