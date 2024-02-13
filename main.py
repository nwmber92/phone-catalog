import connector as con
import users
import phones

#Проверка вводимых значений на числовой тип
def input_check(_value):
    while True:
        if not _value.isnumeric():
            _value = input("Введите целочисленное значение: ")
        else:
            break
    return _value


while True:

    #Консоль доступа в систему
    print("\nДоступные команды:")
    print("1 | логин")
    print("2 | регистрация")
    print("0 | выход")

    command = input("\nВведите команду для продолжения: ")

    if command == "1":

        login = input("Введите логин: ")
        pswd = input("Введите пароль: ")

        # Проверки наличия пользователя и его роли в системе
        login_user = users.Login(login, pswd)
        user_exist = login_user.user_exist()
        if user_exist:
            user_role = login_user.user_role()

            # Консоль пользователя
            if user_role == "user":
                print(f"\nВы вошли как {user_role}.")
                print("Доступные команды:")
                print("1 | вывод таблицы товаров")
                print("0 | выход")

                while True:
                    command = input("\nВведите команду: ")

                    # Вывод таблицы товаров
                    if command == "1":
                        print(phones.table_view())

                    # Выход в лобби
                    elif command == "0":
                        break
                    else:
                        print("<Неверная команда>")

            elif user_role == "admin":
                print(f"\nВы вошли как {user_role}. ")

                while True:

                    # Консоль администратора
                    print()
                    print("Доступные команды:")
                    print("1 | вывод таблицы пользователей")
                    print("2 | изменение роли пользователю")
                    print("3 | вывод таблицы товаров")
                    print("4 | добавление товара")
                    print("5 | удаление товара")
                    print("0 | выход")

                    command = input("\nВведите команду: ")

                    # Вывод таблицы пользователей
                    if command == "1":
                        print()
                        print(users.table_view())

                    elif command == "2":

                        # Вывод облегченной таблицы пользователей
                        print()
                        print(users.table_view().get_string(fields=["id", "Логин", "Роль"]))

                        while True:

                            input_id = input("\nВведите доступный id пользователя : ")
                            user_id = input_check(input_id)

                            # Проверка выбора существующего пользователя
                            if (int(user_id) <= len(users.get_user_list())
                                    and int(user_id) != 0):

                                # Консоль назначения роли пользователю
                                print("\nДоступные роли: ")
                                print("0 | user ")
                                print("1 | admin ")
                                new_role = None

                                while True:

                                    value = input("\nВведите команду для назначения роли: ")

                                    if value == "0":
                                        new_role = "user"
                                        users.set_role(new_role, user_id)
                                        print(f"-- Роль '{new_role}' установлена --")
                                        break
                                    elif value == "1":
                                        new_role = "admin"
                                        users.set_role(new_role, user_id)
                                        print(f"-- Роль '{new_role}' установлена --")
                                        break
                                    else:
                                        print("<Неверная команда>")
                                break
                            else:
                                print("<Неверный id>")

                    # Вывод таблицы товаров
                    elif command == "3":
                        print(phones.table_view())

                    # Добавление позиции в список товаров
                    elif command == "4":
                        print()
                        title = input("Введите название телефона: ")
                        ram_input = input("Введите объем оперативной памяти: ")
                        ram = input_check(ram_input)
                        rom_input = input("Введите объем внутренней памяти: ")
                        rom = input_check(rom_input)
                        cpu = input("Введите название процессора: ")
                        phones.add_item(title, ram, rom, cpu)
                        print("-- Товар добавлен --")

                    # Удаление позиции из списка товаров
                    elif command == "5":
                        while True:

                            input_id = input("Введите позицию удаляемого товара: ")
                            item_id = input_check(input_id)

                            # Проверка на наличие удаляемой позиции
                            if (int(item_id) <= len(phones.get_item_list())
                                    and int(item_id) != 0):

                                phones.del_item(item_id)
                                print("-- Товар удален --")
                                break
                            else:
                                print("<Неверный id>")

                    # Выход в лобби
                    elif command == "0":
                        break
                    else:
                        print("<Неверная команда>")
        else:
            print("<Пользователь не найден>")

    # Консоль регистрации пользователя
    elif command == "2":
        print("\nВведите данные для регистрации")
        s_name = input("Введите фамилию: ")
        f_name = input("Введите имя: ")
        patron = input("Введите отчество: ")
        login = input("Введите логин: ")
        pswd = input("Введите пароль: ")

        new_user = users.Registration(s_name, f_name, patron, login, pswd)

        # Проверка логина на уникальность
        if not new_user.login_status():
            new_user.set_user()
            print("-- Пользователь зарегистрирован --")
        else:
            print("<Пользователь с таким логином уже существует>")

    # Закрытие подключения и завершение работы программы
    elif command == "0":
        con.phone_store_connection().close()
        print("-- Сеанс завершен --")
        break
    else:
        print("<Неверная команда>")
