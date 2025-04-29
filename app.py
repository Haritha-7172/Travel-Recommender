import os
import logging
import mysql.connector
from flask import Flask, session


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")


db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'Haritha@07'),
    'database': os.environ.get('DB_NAME', 'travel_recommendation')
}


def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Database connection error: {err}")
        return None
