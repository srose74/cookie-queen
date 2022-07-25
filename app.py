from distutils.log import debug
from flask import Flask, render_template
import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=cookies_db')
SECRET_KEY = os.environ.get('SECRET_KEY', 'some-key')

app = Flask(__name__)
app.secret_key = SECRET_KEY.encode()


@app.route('/')
def index():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    connection.close()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)