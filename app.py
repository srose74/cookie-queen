from distutils.log import debug
from http import cookies
from flask import Flask, render_template, request
from models.data_controller import all_cookies, all_reviews, commit_order_item

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

@app.route('/order_action', methods=['POST', 'GET'])
def add_order_item():
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    quantity = request.form.get('quantity')
    cookie_id = request.form.get('id')
    cookie_name = request.form.get('cookie_name')
    cookie_price = request.form.get('price')
    cookie_url = request.form.get('url')
    
    order_item = {
        "customer_name" :name,
        "customer_email" :email,
        "customer_mobile" :mobile,
        "quanity" :quantity,
        "cookie_id" :cookie_id,
        "cookie_name" :cookie_name,
        "cookie_price" :cookie_price,
        "cookie_URL" :cookie_url
    }

    print(commit_order_item(DATABASE_URL, order_item))
    return render_template("order-review.html", order_item=order_item)

if __name__ == "__main__":
    app.run(debug=True)