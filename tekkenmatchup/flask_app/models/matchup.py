from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Matchup:
    db_name = 'tekken'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.userchar = db_data['userchar'] #decription
        self.opponent = db_data['opponent'] #instructions
        self.move = db_data['move']
        self.punish = db_data['punish']
        self.num_of_frames = db_data['num_of_frames'] #under30
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.report_on = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO matchups ( userchar, opponent, move, punish, num_of_frames, user_id) VALUES ( %(userchar)s,%(opponent)s,%(move)s,%(punish)s,%(num_of_frames)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM matchups LEFT JOIN users ON users.id = matchups.user_id;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_matchups = []
        print(results)
        for row in results:
            matchup = cls(row)
            matchup.first_name = row['first_name']
            matchup.last_name = row['last_name']
            all_matchups.append( matchup )
        return all_matchups
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM matchups WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE matchups SET userchar=%(userchar)s, opponent=%(opponent)s, move=%(move)s, punish=%(punish)s, num_of_frames=%(num_of_frames)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM matchups WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_matchup(matchup):
        is_valid = True
        if len(matchup['userchar']) < 3: #instructions
            is_valid = False
            flash("Please enter userchar name","matchup")
        if len(matchup['opponent']) < 3: #instructions
            is_valid = False
            flash("Please enter opponent name","matchup")
        if len(matchup['move']) < 3: #instructions
            is_valid = False
            flash("Please enter move name","matchup")
        if len(matchup['punish']) < 1: #instructions
            is_valid = False
            flash("Please enter punishing move name","matchup")
        if len(matchup['num_of_frames']) <1:
            is_valid = False
            flash("Please enter frames of opponents move","matchup")
        return is_valid

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT first_name, last_name from matchups LEFT JOIN users on users.id = matchups.user_id WHERE matchups.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        #breakpoint()
        reports = []
        for row in results:
            data = {
                'first_name' : row['first_name'],
                'last_name' : row['last_name']
            }
            reports.append(data)
        print(reports)
        return reports[0]