from dotenv import load_dotenv
import os, urllib.parse

load_dotenv(dotenv_path='.env.local')
username = os.getenv("DB_USER")
password = urllib.parse.quote(os.getenv("DB_PASS"))
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

jwt_secret_key = os.getenv("JWT_SECRET_KEY")