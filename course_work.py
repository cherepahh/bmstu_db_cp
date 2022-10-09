from logging import logProcesses
import winsound
from matplotlib.cbook import delete_masked_points
import psycopg2
from psycopg2 import Error
import random
from prettytable import PrettyTable
from requests import request

print("\
╔═╗ ╔╗╔╗ ╔╗╔╗        ╔═══╗╔════╗╔═══╗╔════╗╔═══╗\n\
║║╚╗║║║║ ║║║║        ║╔═╗║║╔╗╔╗║║╔═╗║║╔╗╔╗║║╔═╗║\n\
║╔╗╚╝║║╚═╝║║║        ║╚══╗╚╝║║╚╝║║ ║║╚╝║║╚╝║╚══╗\n\
║║╚╗║║║╔═╗║║║ ╔╗     ╚══╗║  ║║  ║╚═╝║  ║║  ╚══╗║\n\
║║ ║║║║║ ║║║╚═╝║     ║╚═╝║  ║║  ║╔═╗║  ║║  ║╚═╝║\n\
╚╝ ╚═╝╚╝ ╚╝╚═══╝     ╚═══╝  ╚╝  ╚╝ ╚╝  ╚╝  ╚═══╝")

def existing_log(log_us):
    request = "select count(*) from users where login = %s"
    cursor.execute(request, (log_us,))
    res = cursor.fetchone()
    return res[0]

def existing_mail(mail_us):
    request = "select count(*) from users where mail = %s"
    cursor.execute(request, (mail_us,))
    res = cursor.fetchone()
    return res[0]

def registration_us(name_us, country_us, mail_us, birth_us, log_us, pass_us, type_us):
    insert_query = "('{name}', '{country}', '{mail}', '{birth_year}', '{login}', '{password}', '{type}')".format(
    name=name_us, country=country_us, mail=mail_us, birth_year=birth_us, login=log_us, password=pass_us, type=type_us)
    cursor.execute("INSERT INTO users (name, country, mail, birth_year, login, password, type) VALUES " + insert_query)
    connection.commit()

def log_in(log_us, pass_us):
    request = "select count(*) from users where login = %s and password = %s"
    cursor.execute(request, (log_us, pass_us,))
    res = cursor.fetchone()
    return res[0]

def print_all_players():
    request = "select * from players"
    cursor.execute(request)
    res = cursor.fetchall()
    if res != []:
        table_pl = PrettyTable()
        table_pl.field_names = ["N", "Имя", "Игровой номер", "Год рождения", "Место рождения", "Страна", "Рост", "Вес", "Хват", "Очки", "Голы", "Передачи", "Количество игр", "+/-"]
        for row in res:
            table_pl.add_row([row[0], row[1], row[12], row[3], row[5], row[4], row[6], row[7], row[8], row[9], row[10], row[11], row[13], row[14]])
        print(table_pl)
    else:
        print("\nИгроков нет")

def print_all_teams():
    request = "select * from teams"
    cursor.execute(request)
    res = cursor.fetchall()
    res.sort(key = lambda x : x[0])
    if res != []:
        table_tm = PrettyTable()
        table_tm.field_names = ["N", "Название", "Страна", "Количество игр", "Победы", "Поражения", "Очки", "Разница шайб"]
        for row in res:
            table_tm.add_row(row)
        print(table_tm)
    else:
        print("\nКоманд нет")

def print_player_from_team(team_name):
    request = "select * from players where team_id = (select id from teams where name = %s)"
    cursor.execute(request, (team_name, ))
    res = cursor.fetchall()
    
    if res != []:
        table_pl = PrettyTable()
        table_pl.field_names = ["Имя", "Игровой номер", "Год рождения", "Место рождения", "Страна", "Рост", "Вес", "Хват", "Очки", "Голы", "Передачи", "Количество игр", "+/-"]
        for row in res:
            table_pl.add_row([row[1], row[12], row[3], row[5], row[4], row[6], row[7], row[8], row[9], row[10], row[11], row[13], row[14]])
        print(table_pl)
    else:
        print("\nТаких игроков нет")

def print_team(team_name):
    request = "select * from teams where name = %s"
    cursor.execute(request, (team_name,))
    res = cursor.fetchone()
    if res != []:
        table_tm = PrettyTable()
        table_tm.field_names = ["Название", "Страна", "Количество игр", "Победы", "Поражения", "Очки", "Разница шайб"]
        table_tm.add_row([res[1], res[2], res[3], res[4], res[5], res[6], res[7]])
        print(table_tm)
    else:
        print("\nКоманды с таким названием нет")


def add_player_to_list(player_name, team_name, log_us):
    request = "select id from players where name = %s and team_id = (select id from teams where name = %s)"
    cursor.execute(request, (player_name, team_name,))
    res = cursor.fetchone()
    
    request = "select id from users where login = %s"
    cursor.execute(request, (log_us,))
    res1 = cursor.fetchone()
    
    insert_query = "('{usr_id}', '{player_id}')".format(usr_id = res1[0], player_id = res[0])
    cursor.execute("INSERT INTO favplayers (usr_id, player_id) VALUES " + insert_query)
    connection.commit()

def add_team_to_list(team_name, log_us):
    request = "select id from teams where name = %s"
    cursor.execute(request, (team_name,))
    res = cursor.fetchone()

    request = "select id from users where login = %s"
    cursor.execute(request, (log_us,))
    res1 = cursor.fetchone()
    
    insert_query = "('{usr_id}', '{team_id}')".format(usr_id = res1[0], team_id = res[0])
    cursor.execute("INSERT INTO favteams (usr_id, team_id) VALUES " + insert_query)
    connection.commit()


def del_player_from_list(player_name, team_name, log_us):
    request = "select id from players where name = %s and team_id = (select id from teams where name = %s)"
    cursor.execute(request, (player_name, team_name,))
    res = cursor.fetchone()
    
    request = "select id from users where login = %s"
    cursor.execute(request, (log_us,))
    res1 = cursor.fetchone()
    
    request = "delete from favplayers where usr_id = %s and player_id = %s"
    cursor.execute(request, (res1[0], res[0],))
    connection.commit()


def del_team_from_list(team_name, log_us):
    request = "select id from teams where name = %s"
    cursor.execute(request, (team_name,))
    res = cursor.fetchone()

    request = "select id from users where login = %s"
    cursor.execute(request, (log_us,))
    res1 = cursor.fetchone()
    
    request = "delete from favteams where usr_id = %s and team_id = %s"
    cursor.execute(request, (res1[0], res[0],))
    connection.commit()    

def print_user_list(log_us):
    request = "select player_id from favplayers where usr_id = (select id from users where login = %s)"
    cursor.execute(request, (log_us,))
    res = cursor.fetchall()
    table_pl = PrettyTable()
    table_pl.field_names = ["Имя", "Игровой номер", "Год рождения", "Место рождения", "Страна", "Рост", "Вес", "Хват", "Очки", "Голы", "Передачи", "Количество игр", "+/-"]
    
    for row in res:
        request = "select * from players where id = %s"
        cursor.execute(request, (row[0],))
        res1 = cursor.fetchone()
        table_pl.add_row([res1[1], res1[12], res1[3], res1[5], res1[4], res1[6], res1[7], res1[8], res1[9], res1[10], res1[11], res1[13], res1[14]])
    print("Избранные игроки: ")
    print(table_pl)

    request = "select team_id from favteams where usr_id = (select id from users where login = %s)"
    cursor.execute(request, (log_us,))
    res2 = cursor.fetchall()
    table_tm = PrettyTable()
    table_tm.field_names = ["Название", "Страна", "Количество игр", "Победы", "Поражения", "Очки", "Разница шайб"]
    
    for row in res2:
        request = "select * from teams where id = %s"
        cursor.execute(request, (row[0],))
        res3 = cursor.fetchone()
        table_tm.add_row([res3[1], res3[2], res3[3], res3[4], res3[5], res3[6], res3[7]])
    print("Избранные команды: ")
    print(table_tm)




def find_player_by_name(player_name):
    player_name = '%' + player_name + '%'
    request = "select * from players where lower(name) like lower(%s)"
    cursor.execute(request, (player_name,))
    res = cursor.fetchall()
    if res != []:
        table_pl = PrettyTable()
        table_pl.field_names = ["Имя", "Игровой номер", "Год рождения", "Место рождения", "Страна", "Рост", "Вес", "Хват", "Очки", "Голы", "Передачи", "Количество игр", "+/-"]
        for row in res:
            table_pl.add_row([row[1], row[12], row[3], row[5], row[4], row[6], row[7], row[8], row[9], row[10], row[11], row[13], row[14]])
        print(table_pl)
    else:
        print("\nТаких игроков нет")


def find_team_by_name(team_name):
    team_name = '%' + team_name + '%'
    request = "select * from teams where lower(name) like lower(%s)"
    cursor.execute(request, (team_name,))
    res = cursor.fetchall()
    if res != []:
        table_tm = PrettyTable()
        table_tm.field_names = ["Название", "Страна", "Количество игр", "Победы", "Поражения", "Очки", "Разница шайб"]
        for row in res:
            table_tm.add_row([row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
        print(table_tm)
    else:
        print("\nКоманд с таким названием нет")


def comparison_players(n):
    table_pl = PrettyTable()
    table_pl.field_names = ["Имя", "Игровой номер", "Год рождения", "Место рождения", "Страна", "Рост", "Вес", "Хват", "Очки", "Голы", "Передачи", "Количество игр", "+/-"]
        
    for i in range(n):
        player_name = input("Введите полное имя игрока: ")
        team_name = input("Введите полное название команды: ")

        request = "select * from players where name = %s and team_id = (select id from teams where name = %s)"
        cursor.execute(request, (player_name, team_name,))
        res = cursor.fetchone()
        
        if res != []:
            table_pl.add_row([res[1], res[12], res[3], res[5], res[4], res[6], res[7], res[8], res[9], res[10], res[11], res[13], res[14]])
        else: 
            print("\nТаких игроков нет")
    print(table_pl)


def comparison_teams(n):
    table_tm = PrettyTable()
    table_tm.field_names = ["Название", "Страна", "Количество игр", "Победы", "Поражения", "Очки", "Разница шайб"]

    for i in range(n):
        team_name = input("Введите полное название команды: ")
        request = "select * from teams where name = %s"
        cursor.execute(request, (team_name,))
        res = cursor.fetchone()
        if res != []:
            table_tm.add_row([res[1], res[2], res[3], res[4], res[5], res[6], res[7]])
        else: 
            print("\nКоманд с таким названием нет")
    print(table_tm)


def analyzing_teams():
    request = "select * from teams"
    cursor.execute(request)
    res = cursor.fetchall()
    flag = True
    
    if res != []:
        table_tm = PrettyTable()
        table_tm.field_names = ["Название", "Шанс выйти в плей-офф (%)"]
        max_games = 0
        all_games = 86
        n = 0
        res.sort(key = lambda x: x[6], reverse=True)
        for row in res:
            n = n + 1 
            if row[3] != all_games:
                flag = False
            if row[3] >= max_games:
                max_games = row[3]
            if n == 16:
                points_half_table = row[6]
                wins_half_table = row[4]
            if n == 17:
                points_half_table2 = row[6]
                games_half_table = row[3]

        max_points = 2 * max_games
        schance = 0.0
        n = 0

        for row in res:
            n = n + 1
            schance = row[6] / (max_points / 100)

            if n > 16:
                temp_points = (all_games - row[3]) * 2
                if (temp_points + row[6]) < points_half_table:
                     schance = 0.0
                if (temp_points + row[6]) == points_half_table:
                    if row[4] < wins_half_table:
                        schance = 0.0

            if n <= 16:
                temp_points = (all_games - games_half_table) * 2
                if (temp_points + points_half_table2) < row[6]:
                     schance = 100.0
                     
            if n <= 16 and flag:
                schance = 100.0
            if n > 16 and flag:
                schance = 0.0

            schance = float('{:.2f}'.format(schance))
            table_tm.add_row([row[1], schance])
    else: 
            print("\nКоманд нет")
    print(table_tm)


def check_admin(log_us):
    request = "select type from users where login = %s"
    cursor.execute(request, (log_us,))
    res = cursor.fetchone()
    return res[0]

def check_moderator(log_us):
    request = "select type from users where login = %s"
    cursor.execute(request, (log_us,))
    res = cursor.fetchone()
    return res[0]

def add_player_to_db():
    player_name = input("Введите полное имя игрока: ")
    team = int(input("Введите id команды: "))
    birth_year1 = int(input("Введите год рождения: "))
    birth_place1 = input("Введите место рождения: ")
    country1 = input("Введите представляемую страну: ")
    shoot = input("Введите хват(R/L): ")
    height1 = int(input("Введите рост: "))
    weight1 = int(input("Введите вес: "))
    games1 = int(input("Введите количество сыгранных игр: "))
    points1 = int(input("Введите количество очков: "))
    goals1 = int(input("Введите количество голов: "))
    assists1 = int(input("Введите количество передач: "))
    number1 = int(input("Введите игровой номер: "))
    plusminus1 = int(input("Введите плюс/минус: "))

    insert_query += "('{name}', '{team_id}', '{birth_year}', '{country}', '{birth_place}', {height}, '{weight}', '{shoots}', '{points}', '{goals}', '{assists}', '{number}', '{games}', '{plusminus}')".format(
    name=player_name, team_id=team, birth_year=birth_year1, country=country1, birth_place=birth_place1, height=height1, weight=weight1, shoots=shoot, points=points1,
    goals=goals1, assists=assists1, number=number1, games=games1, plusminus=plusminus1)

    cursor.execute("INSERT INTO players (name, team_id, birth_year, country, birth_place, height, weight, shoots, points, goals, assists, number, games, plusminus) VALUES " + insert_query)
    connection.commit()

def add_team_to_db():
    team_name = input("Введите полное название команды: ")
    country1 = input("Введите страну: ")
    games1 = int(input("Введите количество сыгранных матчей: "))
    points1 = int(input("Введите количество очков: "))
    wins1 = int(input("Введите количество побед: "))
    loses1 = int(input("Введите количество поражений: "))
    diff = int(input("Введите разницу шайб: "))
    
    insert_query += "('{name}', '{country}', '{games}', '{wins}', '{loses}', '{points}', '{gdifference}')".format(
    name=team_name, country=country1, games=games1, wins=wins1, loses=loses1, points=points1, gdifference=diff)
    cursor.execute("INSERT INTO teams (name, country, games, wins, loses, points, gdifference) VALUES " + insert_query)
    connection.commit()


def delete_player_from_db():
    player_id = int(input("Введите id игрока: "))
    request = "delete from players where id = %s"
    cursor.execute(request, (player_id,))
    connection.commit()


def delete_team_from_db():
    team_id = int(input("Введите id команды: "))
    request = "delete from teams where id = %s"
    cursor.execute(request, (team_id,))
    connection.commit()


def update_player_in_db():
    p_id = int(input("Введите id игрока: "))
    team = int(input("Введите id команды: "))
    games1 = int(input("Введите количество сыгранных игр: "))
    points1 = int(input("Введите количество очков: "))
    goals1 = int(input("Введите количество голов: "))
    assists1 = int(input("Введите количество передач: "))
    plusminus1 = int(input("Введите плюс/минус: "))

    request = "update players set team_id = %s, points = %s, goals = %s, assists = %s, games = %s, plusminus = %s where id = %s"
    cursor.execute(request, (team, points1, goals1, assists1, games1, plusminus1, p_id,))
    connection.commit()

def update_team_in_db():
    t_id = int(input("Введите id команды: "))
    games1 = int(input("Введите количество сыгранных матчей: "))
    points1 = int(input("Введите количество очков: "))
    wins1 = int(input("Введите количество побед: "))
    loses1 = int(input("Введите количество поражений: "))
    diff = int(input("Введите разницу шайб: "))

    request = "update teams set games = %s, wins = %s, loses = %s, points = %s, gdifference = %s where id = %s"
    cursor.execute(request, (games1, wins1, loses1, points1, diff, t_id,))
    connection.commit()

def delete_user_from_db():
    user_id = int(input("Введите id пользователя: "))
    request = "delete from users where id = %s"
    cursor.execute(request, (user_id,))
    connection.commit()


def change_user_type():
    user_log = input("Введите логин пользователя, чьи права хотите изменить: ")
    us_type = -1
    print("Вы хотите:\n\
    1 - Сделать пользователя администратором\n\
    2 - Сделать пользователя модератором\n\
    0 - Лишить прав администратора или модератора\n")
    while us_type != 0 and us_type != 1 and us_type != 2:
        us_type = int(input("Ваш выбор: "))

        if us_type < 0 or us_type > 2:
            print("Повторите попытку.")

    request = "update users set type = %s where login = %s"
    cursor.execute(request, (us_type, user_log,))
    connection.commit


regs = 0 #regs = 1 - user logged; regs = 0 - user not logged
log_us = ""
pass_us = ""
systemstatus = 1  #systemstatus = 1 - working; systemstatus = 0 - exit
checking_log = 1
checking_mail = 1
mailstatus = 1
workstatus = 1
admin_status = 0
moderator_status = 0

try:
    connection = psycopg2.connect(user="postgres",
                                  password="1234",  # Your PostgreSQL passward
                                  host="localhost",  # Your DB host
                                  port="5432",  # Your PostgreSQL port
                                  database="db_cp")

    cursor = connection.cursor()
    while True:

        #sign in and log in
        while systemstatus and not regs:
            print("\nМеню (Выберите пункт): \n\
    1 - Зарегистрироваться \n\
    2 - Войти \n\
    0 - Завершить программу\n")
            systemstatus = int(input("Ваш выбор: "))

            if systemstatus == 1:
                name_us = input("\nВведите ваши имя и фамилию: ")
                country_us = input("Введите вашу страну: ")
                birth_us = int(input("Введите ваш год рождения: "))
                while checking_log:
                    log_us = input("Придумайте логин: ")
                    if existing_log(log_us):
                        print("Данный логин уже существует. Попробуйте снова.")
                    else:
                        checking_log = 0
                pass_us = input("Придумайте пароль: ")
                while checking_mail:
                    mail_us = input("Введите ваш адрес электронной почты: ")
                    if existing_mail(mail_us):
                        print("\nДанный электронный адрес уже используется, выберете действие: \n\
    1 - Ввести другой адрес электронной почты \n\
    2 - Войти с данным адресом электронной почты \n\
    0 - Завершить программу \n")
                        mailstatus = int(input(""))
                        if mailstatus == 1:
                            mail_us = input("Введите ваш адрес электронной почты: ")
                            if existing_mail(mail_us):
                                print("\nДанный электронный адрес также уже используется, попробуйте войти.")
                                continue
                            else:
                                mailstatus = 0
                                checking_mail = 0
                        if mailstatus == 2:
                            continue
                        if mailstatus == 0:
                            exit()
                    else:
                        checking_mail = 0
                registration_us(name_us, country_us, mail_us, birth_us, log_us, pass_us, 0)
                regs = 1

            if systemstatus == 2:
                log_us = input("\nВведите логин: ")
                pass_us = input("\nВведите пароль: ")
                if log_in(log_us, pass_us):
                    regs = 1
                else:
                    print("Неверный логин или пароль. Попробуйте зарегистрироваться или войти снова.")
        
            if systemstatus > 2:
                print("Такого пункта нет. Повторите попытку.")

            if systemstatus == 0:
                exit()
    
        #working
        while systemstatus and regs:
            print("\nМеню (Выберите пункт): \n\
     1 - Показать статистику всех игроков \n\
     2 - Показать статистику всех команд \n\
     3 - Показать статистику игроков определенной команды\n\
     4 - Показать статистику определенной команды\n\
     5 - Добавить игрока в избранное\n\
     6 - Добавить команду в избранное\n\
     7 - Удалить игрока из избранного\n\
     8 - Удалить команду из избранного\n\
     9 - Показать список команд и игроков в избранном\n\
    10 - Найти игрока по имени\n\
    11 - Найти команду по названию\n\
    12 - Сравнить статистику игроков\n\
    13 - Сравнить статистику команд\n\
    14 - Анализ текущих шансов команд в плей-офф\n\
    15 - Перейти в режим модератора\n\
    16 - Перейти в режим администратора\n\
    17 - Выйти из аккаунта\n\
     0 - Завершить работу программы\n")
            systemstatus = int(input("Ваш выбор: "))
        
            if systemstatus == 1:
                print_all_players()
        
            if systemstatus == 2:
                print_all_teams()
        
            if systemstatus == 3:
                team_name = input("Введите полное название команды: ")
                print_player_from_team(team_name)

            if systemstatus == 4:
                team_name = input("Введите полное название команды: ")
                print_team(team_name)

            if systemstatus == 5:
                player_name = input("Введите полное имя игрока: ")
                team_name = input("Введите полное название его команды: ")
                add_player_to_list(player_name, team_name, log_us)

            if systemstatus == 6:
                team_name = input("Введите полное название команды: ")
                add_team_to_list(team_name, log_us)
            
            if systemstatus == 7:
                player_name = input("Введите полное имя игрока: ")
                team_name = input("Введите полное название его команды: ")
                del_player_from_list(player_name, team_name, log_us)

            if systemstatus == 8:
                team_name = input("Введите полное название команды: ")
                del_team_from_list(team_name, log_us)

            if systemstatus == 9:
                print_user_list(log_us)

            if systemstatus == 10:
                player_name = input("Введите имя или часть имени игрока: ")
                find_player_by_name(player_name)

            if systemstatus == 11:
                team_name = input("Введите название или часть названия команды: ")
                find_team_by_name(team_name)

            if systemstatus == 12:
                n = int(input("Вводите количество игроков для сравнения: "))
                comparison_players(n)

            if systemstatus == 13:
                n = int(input("Вводите количество команд для сравнения: "))
                comparison_teams(n)
        
            if systemstatus == 14:
                analyzing_teams()

            if systemstatus == 15:
                if check_moderator(log_us):
                    moderator_status = 1
                else:
                    print("Недостаточно прав.")

            if systemstatus == 16:
                if (check_admin(log_us) == 1):
                    admin_status = 1
                else:
                    print("Недостаточно прав.")

            if systemstatus == 17:
                regs = 0

            if systemstatus > 17:
                print("Такого пункта нет. Повторите попытку.")

            if systemstatus == 0:
                exit()

            while moderator_status:
                print("Меню (Выберите пункт):\n\
    1 - Добавить игрока\n\
    2 - Добавить команду\n\
    3 - Удалить игрока\n\
    4 - Удалить команду\n\
    5 - Обновить статистику игрока\n\
    6 - Обновить статистику команды\n\
    7 - Вернуться в режим пользователя\n")
                moderator_status = int(input("Ваш выбор: "))

                if moderator_status == 1:
                    add_player_to_db()

                if moderator_status == 2:
                    add_team_to_db()
            
                if moderator_status == 3:
                    delete_player_from_db()

                if moderator_status == 4:
                    delete_team_from_db()

                if moderator_status == 5:
                    update_player_in_db()

                if moderator_status == 6:
                    update_team_in_db()
            
                if moderator_status == 7:
                    moderator_status = 0

                if moderator_status > 7:
                    print("Такого пункта нет. Повторите попытку.")  

            while admin_status:
                print("Меню (Выберите пункт):\n\
    1 - Добавить игрока\n\
    2 - Добавить команду\n\
    3 - Удалить игрока\n\
    4 - Удалить команду\n\
    5 - Обновить статистику игрока\n\
    6 - Обновить статистику команды\n\
    7 - Удалить пользователя\n\
    8 - Изменить права доступа пользователя\n\
    9 - Вернуться в режим пользователя\n")
                admin_status = int(input("Ваш выбор: "))

                if admin_status == 1:
                    add_player_to_db()

                if admin_status == 2:
                    add_team_to_db()
            
                if admin_status == 3:
                    delete_player_from_db()

                if admin_status == 4:
                    delete_team_from_db()
                
                if admin_status == 5:
                    update_player_in_db()

                if admin_status == 6:
                    update_team_in_db()
            
                if admin_status == 7:
                    delete_user_from_db()

                if admin_status == 8:
                    change_user_type()
            
                if admin_status == 9:
                    admin_status = 0

                if admin_status > 9:
                    print("Такого пункта нет. Повторите попытку.")    
    


except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")