#все что касается регистрации нового пользователя и авторизации старого
import psycopg2
from player import  *
import random
from contextlib import closing
from wantnewgame import *
#если все норм вернем 1, если имя занято вернем 0

def ckeck_in(log,pasw):

    # сперва подключимся к базе
    with closing(psycopg2.connect(dbname='for_client', user='man', password='qwerty', host='localhost')) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM users where login=%s;""", (log,))
            # проверяем занято ли имя
            if len(cursor.fetchall()):
                # если имя занято
                cursor.close()
                conn.close()
                return 0
            # если все норм то заносим его в базу данных
            cursor.execute("""INSERT INTO users VALUES (%s,%s, %s);""", (log, pasw, 0,))
            cursor.close()
            conn.close()
            return 1


#если все норм вернем 1 и токен, если пароль не верный то 0 если клиент с этой учетки сидит уже то кинем 2
#
def authoriz(log,pasw,client_adr):
    #сперва проверим не зашел ли этот клиент уже с другого устройства
    if name_in_play(log):
        return 2,0
    #дальше проверим правильность пароля/логина в бд
     # сперва подключимся к базе

    # сперва подключимся к базе
    with closing(psycopg2.connect(dbname='for_client', user='man', password='qwerty', host='localhost')) as conn:
        with conn.cursor() as cursor:

            cursor.execute("""SELECT * FROM users where login=%s and password=%s;""", (log, pasw))

            v = cursor.fetchall()
            if len(v):
                # если логин и пароль верные
                cursor.close()
                conn.close()
                # генерируем токен для игрока
                tok = int(random.uniform(0, 1000000))
                while tok in [i.token for i in list_of_player]:
                    tok = int(random.uniform(0, 1000000))
                # создаем игрока
                Player(log, v[0][2], tok, client_adr[0], client_adr[1])
                return 1, tok
            # если логин и пароль неверные
            return 0, 0
