import psycopg2 as db
from main import config
import random


class Database:
    def __init__(self):
        self.conn = db.connect(
            database=config.DB_NAME,
            password=config.DB_PASS,
            user=config.DB_USER,
            host=config.DB_HOST
        )
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.conn.commit()
        user_table = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT NOT NULL,
        full_name VARCHAR(55),
        phone_number VARCHAR(13),
        status BOOLEAN DEFAULT false
        )
        """

        challenges = """
        CREATE TABLE IF NOT EXISTS challenges (
        challenge_id SERIAL PRIMARY KEY,
        owner_id BIGINT,
        user_id BIGINT,
        start_at DATE,
        full_date INT  CHECK (full_date > 0),
        end_date DATE,
        limited_time INT  CHECK (limited_date > 0),
        mission TEXT,
        status BOOLEAN DEFAULT false)
        """

      

        self.cursor.execute(user_table)
        self.cursor.execute(challenges)

        self.conn.commit()

