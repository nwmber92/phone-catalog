import connector as con
from prettytable import PrettyTable

# Установка подключения к БД
connection = con.phone_store_connection()

# Добавление данных в БД
def add_item(title, ram, rom, cpu):
    q = "INSERT INTO phones (title, ram, rom, cpu) VALUES(%s, %s, %s, %s)"
    phone = (title, ram, rom, cpu)
    con.execute_query(connection, q, phone)

# Удаление данных из БД и сброс счетчика нумерации
def del_item(item_id):
    q = """
    DELETE FROM phones WHERE id = %s;
    ALTER SEQUENCE phones_id_seq RESTART;
    UPDATE phones SET id = DEFAULT;
    """
    con.execute_query(connection, q, item_id)

# Получение списка всех смартфонов
def get_item_list():
    q = "SELECT * FROM phones ORDER BY id ASC"
    result = con.select_query(connection, q)
    item_list = []

    for i in result:
        item_list.append(i)

    return item_list

# Инициализация таблицы смартфонов в консоле
def table_view():
    t = PrettyTable()
    t.field_names = ["id", "Название", "Оперативная память", "Внутренняя память", "Процессор"]
    t.add_rows(get_item_list())
    return t


if __name__ == "__main__":

    # Инициализация таблицы смартфонов в БД
    phone_table = """
    CREATE TABLE IF NOT EXISTS phones (
      id SERIAL PRIMARY KEY,
      title VARCHAR(50) NOT NULL,
      ram INT NOT NULL,
      rom INT NOT NULL,
      cpu VARCHAR(50) NOT NULL
    )
    """
    con.execute_query(connection, phone_table)

    # Добавление смартфонов в БД
    items = [
        ("POCO X3 Pro", "8", "256", "Qualcomm Snapdragon 860"),
        ("Xiaomi Redmi Note 11S", "8", "128", "MediaTek Helio G96"),
        ("HUAWEI Nova 9 SE", "8", "128", "Qualcomm Snapdragon 680"),
        ("Realme 9 Pro+", "8", "256", "MediaTek Dimensity 920"),
        ("OnePlus 9", "12", "256", "Qualcomm Snapdragon 888")
    ]

    for item in items:
        add_item(*item)

    print(table_view())

    # Закрытие подключения
    if connection:
        connection.close()
