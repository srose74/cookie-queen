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

def commit_order_item(database_url, order_item):

    #1. Check if customer exists, if no create new customer record, if yes find customer id
    customer_info = sql_select_params(database_url, "SELECT * FROM customers WHERE email = %s", [order_item['customer_email']])
    if customer_info:
        customer_id = customer_info[0][0]
        print(customer_id)
    else:
        print("Customer does not exist")
        sql_write(database_url, "INSERT INTO customers (name, email, mobile) VALUES (%s, %s, %s)", (order_item['customer_name'], order_item['customer_email'], order_item['customer_mobile']))

    #2. Check if custoer has a pending order, if no create new order, if yes find order id
    #3. Commit order to order items.


  
