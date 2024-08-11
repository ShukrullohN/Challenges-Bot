
from decouple import config

ADMINS = config("ADMIN")
TOKEN = config('TOKEN')
DB_NAME = config("DB_NAME")
DB_PORT = config("DB_PORT")
DB_HOST = config("DB_HOST")
DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")

