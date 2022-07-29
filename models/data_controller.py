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

def review_order(database_url, order_details):
    customer_id = order_details[1]
    order_id = order_details[0]
    print(customer_id)
    print (order_id)

def commit_order_item(database_url, order_item):

    #1. Check if customer exists, if no create new customer record, if yes find customer id
    customer_info = sql_select_params(database_url, "SELECT * FROM customers WHERE email = %s", [order_item['customer_email']])
    if customer_info:
        customer_id = customer_info[0][0]
    else:
        print("Customer does not exist")
        sql_write(database_url, "INSERT INTO customers (name, email, mobile) VALUES (%s, %s, %s)", (order_item['customer_name'], order_item['customer_email'], order_item['customer_mobile']))
        customer_info = sql_select_params(database_url, "SELECT id FROM customers WHERE email=%s;", [order_item['customer_email']])
        customer_id = customer_info[0][0]

    #2. Check if customer has a pending order, if no create new order, if yes find order id   
    order_info = sql_select_params(database_url, "SELECT * FROM orders WHERE customer_ID = %s", [customer_id])
    if order_info and order_info[0][3] == 'PENDING':
        order_id = order_info[0][0]
    else:
        print("Order does not exist")
        sql_write(database_url, "INSERT INTO orders (customer_id, order_total, order_status) VALUES (%s, %s, %s)", (customer_id, 0, 'PENDING'))
        order_info = sql_select_params(database_url, "SELECT id FROM orders WHERE customer_ID = %s and order_status = %s", [customer_id, 'PENDING'])
        order_id = order_info[0][0]
    
    #3. Commit order to order items.
    cookie_price = float(order_item['cookie_price'])
    cookie_id = int(order_item['cookie_id'])
    quantity = int(order_item['quantity'])
    order_item_total = (cookie_price*100) * quantity  
    sql_write(database_url, "INSERT INTO order_items (order_id, cookie_id, quantity, price_in_cents) VALUES (%s, %s, %s, %s)", (order_id, cookie_id, quantity, order_item_total))

    #4. Calculate order total and update
    order_total = sql_select_params(database_url, "SELECT order_total FROM orders WHERE id = %s", [order_id])
    updated_order_total = order_total[0][0] + order_item_total
    sql_write(database_url, "UPDATE orders SET order_total=%s WHERE id=%s ", [updated_order_total, order_id])
    print("order_item commited to database")

    order_details = [customer_id, order_id]
    return order_details


  
