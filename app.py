from distutils.log import debug
from http import cookies
from flask import Flask, render_template
from models.data_controller import all_reviews

import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=cookies_db')
SECRET_KEY = os.environ.get('SECRET_KEY', 'some-key')

app = Flask(__name__)
app.secret_key = SECRET_KEY.encode()


@app.route('/')
def index():
    reviews = all_reviews(DATABASE_URL)
    return render_template("index.html", reviews=reviews)

@app.route('/cookies')
def display_cookies():
    return render_template ("cookies.html")

if __name__ == "__main__":
    app.run(debug=True)