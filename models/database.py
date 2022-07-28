import psycopg2

def sql_select(database_url, query):
    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def sql_select_params(database_url, query, params):
    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def sql_write(database_url, query, params):
    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    connection.close()
    print("record written to database")
  


