import connector as con
from prettytable import PrettyTable

# Установка подключения к БД
connection = con.phone_store_connection()


class Registration:

    def __init__(self, s_name, f_name, patron, login, pswd):
        self.s_name = s_name
        self.f_name = f_name
        self.patron = patron
        self.login = login
        self.pswd = pswd
        self.role = "user"
        self.exist = True
    
    # Добавление пользователя в БД
    def set_user(self):
        q = """
        INSERT INTO users (s_name, f_name, patron, login, pswd, role, exist) 
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            self.s_name,
            self.f_name,
            self.patron,
            self.login,
            self.pswd,
            self.role,
            self.exist
        )

        con.execute_query(connection, q, values)
    
    # Проверка логина на наличие в системе
    def login_status(self) -> bool:
        q = "SELECT EXISTS(SELECT 1 FROM users WHERE login = %s)"
        values = (self.login,)
        result = con.select_query(connection, q, values, "1")
        return result[0]


class Login:

    def __init__(self, login, pswd):
        self.login = login
        self.pswd = pswd
    
    # Проверка пользовательского статуса в системе
    def user_exist(self):
        q = "SELECT exist FROM users WHERE login = %s AND pswd = %s"
        values = (self.login, self.pswd)
        result = con.select_query(connection, q, values, "1")
        if result:
            return True
        else:
            return False
    
    # Получение роли пользователя в системе
    def user_role(self):
        q = "SELECT role FROM users WHERE login = %s AND pswd = %s"
        values = (self.login, self.pswd)
        result = con.select_query(connection, q, values, "1")
        return result[0]

# Получение списка всех пользователей 
def get_user_list():
    q = "SELECT * FROM users ORDER BY id ASC"
    result = con.select_query(connection, q)
    user_list = []

    for _user in result:
        user_list.append(_user)

    return user_list

# Назначение роли пользователю
def set_role(new_role, user_id):
    q = "UPDATE users SET role = %s WHERE id = %s"
    values = (new_role, user_id)
    con.execute_query(connection, q, values)

# Инициализация таблицы пользователей в консоле
def table_view():
    t = PrettyTable()
    t.field_names = [
        "id",
        "Имя",
        "Фамилия",
        "Отчество",
        "Логин",
        "Пароль",
        "Роль",
        "Статус"
    ]
    t.add_rows(get_user_list())
    return t


if __name__ == "__main__":
    
    # Инициализация таблицы пользователей в БД
    create_table = """
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      s_name VARCHAR(30) NOT NULL,
      f_name VARCHAR(30) NOT NULL,
      patron VARCHAR(30) NOT NULL,
      login VARCHAR(30) NOT NULL UNIQUE,
      pswd VARCHAR(12) NOT NULL,
      role VARCHAR(10) NOT NULL,
      exist BOOL NOT NULL)
    """
    con.execute_query(connection, create_table)

    # Добавление пользователей в БД
    users = [
        ("Вердеревский", "Серафим", "Викторович", "admin", "admin"),
        ("Ясырев", "Ефим", "Арсеньевич", "efim31", "1ab1c"),
        ("Митина", "Анфиса", "Степановна", "anfisa41", "6d028"),
        ("Морошкин", "Марк", "Петрович", "mark22", "ee3425")
    ]
    
    for user in users:
        Registration(*user).set_user()
    
    # Назначение администратора
    set_role("admin", "1")

    print(table_view())
    
    # Закрытие подключения
    if connection:
        connection.close()
