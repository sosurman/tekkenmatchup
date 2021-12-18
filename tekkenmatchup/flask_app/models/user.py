from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class User:
    db_name = 'tekken'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return User(results[0])

    # @classmethod
    # def get_friendship(cls,data):
    #     query = "SELECT * FROM friends WHERE id = %(id)s;"
    #     results = connectToMySQL(cls.db_name).query_db(query,data)
    #     if len(results) < 1:
    #         return False
    #     return User(results[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 3:
            is_valid = False
            flash("First name must be at least 3 characters.","register")
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters.","register")
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid Email Address.","register")
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters.","register")
        if user['password'] != user['confirm']:
            is_valid = False
            flash("Passwords do not match!","register")
        return is_valid


class Friend:
    db_name = 'tekken'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.friend_id = db_data['friend_id']

    @classmethod
    def get_all(cls,data):
        # breakpoint()
        query = f"SELECT * FROM friends where user_id = {data['id']};"
        results = connectToMySQL(cls.db_name).query_db(query)
        friends = []
        # if len(results) < 1:
        #     return False
        for friend in results:
            friends.append(cls(friend))
        return friends

    @classmethod
    def savefriendship(cls,data):
        query = "INSERT INTO friends (user_id, friend_id, created_at,updated_at) VALUES (%(id)s,%(friend_id)s,NOW(),NOW());"
        return connectToMySQL(cls.db_name).query_db(query,data)