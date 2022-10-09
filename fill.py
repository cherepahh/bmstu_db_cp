from logging import logProcesses
import winsound
import psycopg2
from psycopg2 import Error
import random

names = ["Teddy Blueger",
         "Brian Boyle",
         "Jeff Carter",
         "Sidney Crosby",
         "Jake Guentzel",
         "Danton Heinen",
         "Kasperi Kapanen",
         "Evgeni Malkin",
         "Brock McGinn",
         "Drew OConnor",
         "Rickard Rackell",
         "Evan Rodrigues",
         "Brian Rust",
         "Radim Zohorna",
         "Jason Zucker",
         "Nathan Beaulieu",
         "Brian Dumoulin",
         "Mark Friedman",
         "Kris Letang",
         "John Marino",
         "Mark Matheson",
         "Chad Ruhwedel",
         "Alex DOrio",
         "Casey DeSmith",
         "Louis Domingue",
         "Tristan Jarry",
         "Nicolas Aube-Kubel",
         "Andre Burakovsky",
         "Gabriel Landeskog",
         "Carl Hagelin",
         "Juuso Riikola",
         "Nathan McKinnon",
         "Alex Newhook",
         "Bowen Byram",
         "Valeri Nichushkin",
         "Cale Makar",
         "Dylan Cozens",
         "Rasmus Dahlin",
         "Matthew Murray",
         "Marc-Andre Fleury",
         "Nico Hischier",
         "Ben Meyers",
         "Dowson Mercer",
         "Mackenzie Blackwood"]

countries = ["USA",
           "Russia",
           "Canada",
           "Finland",
           "Sweden",
           "Latvia",
           "Denmark",
           "Switzerland",
           "Norway",
           "Belarus",
           "Slovakia",
           "Czech Republic"]

names_t = ["Anaheim Ducks",
           "Arizona Coyotes",
           "Boston Bruins",
           "Buffalo Sabres",
           "Calgary Flames",
           "Carolina Hurricanes",
           "Chicago Blackhawks",
           "Colorado Avalanche",
           "Columbus Blue Jackets",
           "Dallas Stars",
           "Detroit Red Wings",
           "Edmonton Oilers",
           "Florida Panthers",
           "Los Angeles Kings",
           "Minnesota Wild",
           "Montreal Canadiens",
           "Nashville Predators",
           "New Jersey Devils",
           "New York Islanders",
           "New York Rangers",
           "Ottawa Senators",
           "Philadelphia Flyers",
           "Pittsburgh Penguins",
           "San Jose Sharks",
           "Seattle Kraken",
           "St. Louis Blues",
           "Tampa Bay Lightning",
           "Toronto Maple Leafs",
           "Vancouver Canucks",
           "Vegas Golden Knigts",
           "Washington Capitals",
           "Winnipeg Jets"]

team_c = ["USA", "Canada"]

work_hand = ["Right", "Left"]

mails = ["test", "yandex", "gmail", "pochta", "testtest",
         "yapochta", "ya", "bk", "yahoo", "duckduck"]

dom_mail = ["ru", "com", "bu", "ua", "ca", "se", "du", "bz", "be", "bm", "au", "at", "az", "al",
            "am", "id", "iq", "ir", "is", "ie", "es", "it", "kz", "kh", "cn", "cu", "lv", "lu"]

logn_us = ["q", "w", "e", "t", "y", "a", "s", "d", "f", "g", "r", "u", "i", "o", "p", "h", "j", "k",
           "l", "z", "x", "c", "v", "b", "n", "m", "qq", "ww", "ee", "rr", "tt", "yy", "uu", "ii",
           "oo", "pp", "aa", "ss", "dd", "ff", "gg", "hh", "jj", "kk", "ll", "zz", "xx", "cc", "vv", 
           "bb", "nn", "mm", "asd", "qwe", "zxc", "rty", "fgh", "vbn", "uio", "jkl", "mpl"]

passw = ["1234", "4321", "1234", "4321", "1234", "4321", "1234", "4321", "1234", "1111", 
          "q", "w", "e", "t", "y", "a", "s", "d", "f", "g", "r", "u", "i", "o", "p", "h", "j", "k",
           "l", "z", "x", "c", "v", "b", "n", "m", "qq", "ww", "ee", "rr", "tt", "yy", "uu", "ii",
           "oo", "pp", "aa", "ss", "dd", "ff", "gg", "hh", "jj", "kk", "ll", "zz", "xx", "cc", "vv", 
           "bb", "nn", "mm", "asd", "qwe", "zxc", "rty", "fgh", "vbn", "uio", "jkl", "mpl"]

try:
    connection = psycopg2.connect(user="postgres",
                                  password="1234",  # Your PostgreSQL passward
                                  host="localhost",  # Your DB host
                                  port="5432",  # Your PostgreSQL port
                                  database="db_cp")

    count_players = int(input("hockey players: "))
    count_teams = 32
    us_count=1000
    n = 1000

    cursor = connection.cursor()
    points1 = 0
    goals1 = 0
    k=0

    if count_teams:
        insert_query = ""
        for i in range(count_teams):
            loses1 = random.randint(1, 5)
            wins1 = random.randint(5, 10)
            insert_query += "('{name}', '{country}', '{games}', '{wins}', '{loses}', '{points}', '{gdifference}'),".format(
                name=names_t[k],
                country=random.choice(team_c),
                games=loses1+wins1,
                wins=wins1,
                loses=loses1,
                points=wins1*2,
                gdifference=random.randint(-50, 50))
            k=k+1

        cursor.execute(
            "INSERT INTO teams (name, country, games, wins, loses, points, gdifference) VALUES " + insert_query[:-1])
        connection.commit()

    if count_players:
        insert_query = ""
        for i in range(count_players):
            goals1 = random.randint(0, 30)
            assists1 = random.randint(0, 15)
            insert_query += "('{name}', '{team_id}', '{birth_year}', '{country}', '{birth_place}', {height}, '{weight}', '{shoots}', '{points}', '{goals}', '{assists}', '{number}', '{games}', '{plusminus}'),".format(
                name=random.choice(names),
                team_id=random.randint(1, 31),
                birth_year=random.randint(1981, 2004),
                country=random.choice(countries),
                birth_place=random.choice(countries),
                height=random.randint(170, 220),
                weight=random.randint(60, 115),
                shoots=random.choice(work_hand),
                points=goals1+assists1,
                goals=goals1, 
                assists=assists1,
                number=random.randint(2, 98),
                games=random.randint(10, 50),
                plusminus=random.randint(-5, 10))

        cursor.execute(
            "INSERT INTO players (name, team_id, birth_year, country, birth_place, height, weight, shoots, points, goals, assists, number, games, plusminus) VALUES " + insert_query[:-1])
        connection.commit()

    if us_count:
        insert_query = ""
        for i in range(us_count):
            insert_query += "('{name}', '{country}', '{mail}', '{birth_year}', '{login}', '{password}', '{type}'),".format(
                name=random.choice(names),
                country=random.choice(countries),
                mail=random.choice(logn_us) + "@" + random.choice(mails) + "." +random.choice(dom_mail),
                birth_year=random.randint(1923, 2009),
                login=random.choice(logn_us) + random.choice(logn_us),
                password=random.choice(passw),
                type=0)

        cursor.execute(
            "INSERT INTO users (name, country, mail, birth_year, login, password, type) VALUES " + insert_query[:-1])
        connection.commit()

    if n:
        insert_query = ""
        for i in range(n):
            insert_query += "('{usr_id}', '{player_id}'),".format(
                usr_id=random.randint(1, 10),
                player_id=random.randint(1, 1000))

        cursor.execute(
            "INSERT INTO favplayers (usr_id, player_id) VALUES " + insert_query[:-1])
        connection.commit()

    if n:
        insert_query = ""
        for i in range(n):
            insert_query += "('{usr_id}', '{team_id}'),".format(
                usr_id=random.randint(1, 10),
                team_id=random.randint(1, 32))

        cursor.execute(
            "INSERT INTO favteams (usr_id, team_id) VALUES " + insert_query[:-1])
        connection.commit()

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
