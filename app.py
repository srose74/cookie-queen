from distutils.log import debug
from http import cookies
from flask import Flask, render_template, request
from models.data_controller import all_cookies, all_reviews

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
    cookies = all_cookies(DATABASE_URL)
    return render_template ("cookies.html", cookies_list=cookies)

@app.route('/orders', methods=['GET'])
def order():
    cookie_id = request.args.get('id')
    cookie_name = request.args.get('name')
    cookie_price = request.args.get('price')
    cookie_url = request.args.get('url')

    return render_template("orders.html", cookie_id=cookie_id, cookie_name=cookie_name, cookie_price=cookie_price, cookie_url=cookie_url)

@app.route('/order_action', methods=['POST'])
def add_order_item():
    quantity = request.args.get('quantity')
    print(quantity)
    return render_template("order-review.html")

if __name__ == "__main__":
    app.run(debug=True)