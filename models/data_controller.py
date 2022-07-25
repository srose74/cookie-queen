from models.database import sql_select

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




