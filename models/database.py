import psycopg2

def sql_select(database_url, query):
    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.close()




