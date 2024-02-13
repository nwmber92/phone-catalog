import psycopg2

# Создание подключения
def create_connection(db_name, db_user, db_password, db_host, db_port):
    con = None
    try:
        con = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
    except Exception as e:
        print(e)
    return con

# Инициализация БД
def create_database(db_con, query):
    db_con.autocommit = True
    c = db_con.cursor()
    try:
        c.execute(query)
        print("-- База данных установлена --")
    except Exception as e:
        print(e)

# Обработка запроса
def execute_query(db_con, query, values=None):
    c = db_con.cursor()
    try:
        c.execute(query, values)
        db_con.commit()
    except Exception as e:
        print(e)

# Обработка вывода запроса
def select_query(db_con, query, values=None, fetch="*"):
    c = db_con.cursor()
    result = None
    try:
        c.execute(query, values)
        if fetch == "*":
            result = c.fetchall()
        elif fetch == "1":
            result = c.fetchone()
        return result
    except Exception as e:
        print(e)

# Создание подключения к БД проекта
def phone_store_connection():
    con = create_connection(
        "phone_store", "postgres", "admin", "127.0.0.1", "5432"
    )
    return con


if __name__ == "__main__":

    # Создание подключения к БД по умолчанию
    connection = create_connection(
        "postgres", "postgres", "admin", "127.0.0.1", "5432"
    )

    # Установка БД проекта
    db_query = "CREATE DATABASE phone_store"
    create_database(connection, db_query)

    # Закрытие подключения
    if connection:
        connection.close()
