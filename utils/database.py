import psycopg2 as db
from main import config
import random
from datetime import timedelta

# self.conn.commit()

class Database:
    def __init__(self):
        self.conn = db.connect(
            database=config.DB_NAME,
            password=config.DB_PASS,
            user=config.DB_USER,
            host=config.DB_HOST
        )
        self.cursor = self.conn.cursor()


    def add_user(self, data: dict):
        first_name = data["first_name"]
        last_name = data["last_name"]
        chat_id = data["chat_id"]
        username = data["username"]
        phone_number = data["phone_number"]
        query = f"""INSERT INTO users (chat_id, first_name, last_name , phone_number, username, via_register)
        VALUES ({chat_id}, '{first_name}','{last_name}', '{phone_number}', '{username}', 'VIA_BOT')"""
        self.cursor.execute(query)
        self.conn.commit()
        return True

    def get_user_by_chat_id(self, chat_id):
        query = f"SELECT * FROM users WHERE chat_id = '{chat_id}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result


    def get_user_challenges(self, chat_id):
        query = f"select 'id' from users where chat_id = '{chat_id}'"
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        query = f"select * from members where user_id = {user}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    

    def check_username(self, mess):
        query = f"select username from users where username = '{mess}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result
    


    def get_created_challenges(self, user_id):
        query =  f"SELECT * FROM challenges WHERE owner_id = {user_id}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result


    def get_public_challenges(self):
        query =  f"SELECT * FROM challenges WHERE status = TRUE"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result


    def join_challenges(self):
        query =  f"SELECT * FROM members WHERE challenge_id = {challenge_id} AND user_id = {user_id}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
        


    def add_member(self, challenge_id, user_id):
        query = f"insert into members (user, challenges) values('{user_id}', '{challenge_id}')"
        self.cursor.execute(query)
        self.conn.commit()
        return True

    def get_challenge_by_id(self, challenge_id):
        query = f"SELECT * FROM challenges WHERE id = {challenge_id}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def search_challenge_via_secret_key(self, secret_key):
        query = f"SELECT * FROM challenges WHERE secret_key = '{secret_key}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def check_secret_pass(self, challenge_id, secret_pass):
        query =  f"SELECT * FROM challenges WHERE id = {challenge_id} AND secret_pass = '{secret_pass}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def update_first_name(self, new_first_name, user_id):
        query = f"UPDATE users SET first_name = '{new_first_name}' WHERE chat_id = '{user_id}'"
        self.cursor.execute(query)
        self.conn.commit()
        return True
        

    def update_last_name(self, new_last_name, user_id):
        query = f"UPDATE users SET last_name = '{new_last_name}' WHERE chat_id = '{user_id}'"
        self.cursor.execute(query)
        self.conn.commit()
        return True
        
    def update_username(self, new_username, user_id):
        query = f"UPDATE users SET username = '{new_username}' WHERE chat_id = '{user_id}'"
        self.cursor.execute(query)
        self.conn.commit()
        return True

    def update_phone_number(self, new_phone_number, user_id):
        query = f"UPDATE users SET phone_number = '{new_phone_number}' WHERE chat_id = '{user_id}'"
        self.cursor.execute(query)
        self.conn.commit()
        return True


    def save_challenge(self, data: dict):
        name = data["name"]
        owner = data["owner"]
        info = data["info"]
        goal = data["goal"]
        mission = data["mission"]
        start_at = data["start_at"]
        full_time= data["full_time"]
        limited_time = data["limited_time"]
        is_different = data["is_different"]
        status = data["status"]
        secret_key = data.get("secret_key")
        secret_pass = data.get("secret_pass")
        end_at = data['start_at'] + timedelta(days=data['full_time'])

        query  = f"""
        INSERT INTO challenges (name, owner_id, start_at, end_at, full_time, limited_time, is_different, status,  secret_key, secret_password)
        VALUES ('{name}','{owner}', '{start_at}', '{end_at}','{full_time}', '{limited_time}', '{is_different}', '{status}',  '{secret_key}', '{secret_pass}')
        """
        self.cursor.execute(query)
        self.conn.commit
        return True
        