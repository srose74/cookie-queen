from distutils.log import debug
from http import cookies
from flask import Flask, render_template, request, redirect, session
from models.data_controller import all_cookies, all_reviews, commit_order_item, display_order_details, display_order_items, get_user_details

import os
import bcrypt

from models.database import sql_select_params

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
        "quantity" :quantity,
        "cookie_id" :cookie_id,
        "cookie_name" :cookie_name,
        "cookie_price" :cookie_price,
        "cookie_URL" :cookie_url
    }

    order_details = commit_order_item(DATABASE_URL, order_item)
    customer_id = order_details[0]
    order_id = order_details[1]

    order_details = display_order_details(DATABASE_URL, customer_id, order_id)
    order_items = display_order_items (DATABASE_URL, order_id)

    return render_template("order-review.html", order_details=order_details, order_items=order_items)

@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    return render_template("sign_up.html")

@app.route('/signup_action', methods=['POST'])
def signup_action():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(name)
    print(email)
    print(password_hash)

    return redirect('/')

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")

@app.route('/login_action', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')

    user_details = get_user_details(DATABASE_URL, email)

    if user_details:
        print("user exists")
        valid = bcrypt.checkpw(password.encode(), user_details['user_password'].encode())
        print(valid)
        if valid:
            session['user_email'] = user_details['user_email']
            session['username'] = user_details['user_name']
            session['user_id'] = user_details['user_id']
            session['password_hash'] = user_details['user_password']
            return redirect('/')
    else:
        print("user does not exist")
        return redirect('/login')
    
    

if __name__ == "__main__":
    app.run(debug=True)