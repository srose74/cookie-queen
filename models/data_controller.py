from this import d
from typing import ItemsView
from models.database import sql_select, sql_write, sql_select_params

def all_reviews(database_url):
    results = sql_select(database_url, "SELECT * FROM reviews;")
    review_list = []
    for row in results:
        review = {
            'id': row[0],
            'customer_id': row[1],
            'cookie_id': row[2],
            'tag_line': row[3],
            'detailed_review': row[4],
            'rating': row[5]
        }
        review_list.append(review)
    return review_list
    
def all_cookies(database_url):
    results = sql_select(database_url, "SELECT * FROM cookies;")
    cookies_list = []
    for row in results:
        cookies = {
            'id': row[0],
            'name': row[1],
            'image_URL': row[2],
            'price': f'{(row[3]/100):.2f}',
            'category': row[4]
        }
        cookies_list.append(cookies)
    return cookies_list

def get_customer(database_url, email):
    customer_info = sql_select_params(database_url, "SELECT id FROM customers WHERE email = %s", [email])
    if customer_info:    
        customer_id = customer_info[0][0]
        return customer_id
    else:
        return customer_info

def get_order(database_url, customer_id):
    order_info = sql_select_params(database_url, "SELECT id FROM orders WHERE customer_ID = %s", [customer_id])
    if order_info:
        order_id = order_info[0][0]
        return order_id
    else:
        return order_info

def get_order_status(database_url, customer_id):
    order_info = sql_select_params(database_url, "SELECT order_status FROM orders WHERE customer_id = %s", [customer_id])
    if order_info:
        order_status = order_info[0][0]
        return order_status
    else:
        return order_info

def display_order_details(database_url, customer_id, order_id):    
    customer_details = sql_select_params(database_url,"SELECT * FROM customers WHERE id=%s", [customer_id])
    order_total = sql_select_params(database_url, "SELECT order_total FROM orders WHERE id = %s", [order_id])
    order_details = customer_details + order_total
    return order_details

def display_order_items(database_url, order_id):
    order_items = sql_select_params(database_url,"SELECT cookies.name, cookies.image, cookies.price_in_cents, order_items.quantity, order_items.price_in_cents FROM order_items INNER JOIN cookies ON order_items.cookie_id=cookies.id WHERE order_id=%s" , [order_id])
    order_items_list = []
    for row in order_items:
        order_item = {
            'cookie_name': row[0],
            'image_URL': row[1],
            'price': f'{(row[2]/100):.2f}',
            'quantity': row[3],
            'total_price': f'{(row[4]/100):.2f}',
        }
        order_items_list.append(order_item)
    return order_items_list

     
def commit_order_item(database_url, order_item):

    #1. Check if customer exists, if no create new customer record, if yes find customer id
    customer_id = get_customer(database_url, order_item['customer_email'])
    
    if customer_id:
        print('Customer exists')
    else:
        print("Customer does not exist")
        #create customer first
        sql_write(database_url, "INSERT INTO customers (name, email, mobile) VALUES (%s, %s, %s)", (order_item['customer_name'], order_item['customer_email'], order_item['customer_mobile']))
        customer_id = get_customer(database_url, order_item['customer_email'])

    #2. Check if customer has a pending order, if no create new order, if yes find order id   
    order_id = get_order(database_url, customer_id)
    order_status = get_order_status(database_url, customer_id)

    if order_id and order_status == 'PENDING':
        print('Order exists')
    else:
        print("Order does not exist")
        #create order first
        sql_write(database_url, "INSERT INTO orders (customer_id, order_total, order_status) VALUES (%s, %s, %s)", (customer_id, 0, 'PENDING'))
        order_id = get_order(database_url, customer_id)
    
    #3. Commit order to order items
    cookie_price = float(order_item['cookie_price'])
    cookie_id = int(order_item['cookie_id'])
    quantity = int(order_item['quantity'])
    order_item_total = (cookie_price*100) * quantity

    sql_write(database_url, "INSERT INTO order_items (order_id, cookie_id, quantity, price_in_cents) VALUES (%s, %s, %s, %s)", (order_id, cookie_id, quantity, order_item_total))

    #4. Calculate order total and update order
    order_total = sql_select_params(database_url, "SELECT order_total FROM orders WHERE id = %s", [order_id])
    updated_order_total = order_total[0][0] + order_item_total
    sql_write(database_url, "UPDATE orders SET order_total=%s WHERE id=%s ", [updated_order_total, order_id])
    print("order_item commited to database")

    order_details = [customer_id, order_id]
    return order_details


  
