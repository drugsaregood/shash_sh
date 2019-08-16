from consignment import  *
from wantnewgame import *
#то что связано с концом игры
from contextlib import closing
import psycopg2
def are_equal(tok_g):
    #удаляем партию из списка партий
    #у участников остается прежденее количество баллов
    #их состояние переходит в 0
    game=token_in_game(tok_g)
    game.player_white.state=game.player_black.state=0
    list_of_Сonsignment.remove(game)



#игрок сдается
def give_up(tokgame,tokplay):
    #все что при ничьей только сдаюземуся -1 бал а другому +1
    opp=adr_opponent(tokplay, tokplay)
    we=token_in_play(tokplay)
    opp.points+=1
    opp.points -= 1
    are_equal(tokgame)

#игрок нажимает закрыть приложение
def exit_ap(tok):
    #количество баллов у нашего игрока
    we=token_in_play(tok)
    #новое количество баллов должно быть обновлено в бд
    # сперва подключимся к базе
    with closing(psycopg2.connect(dbname='for_client', user='man', password='qwerty', host='localhost')) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM users where login=%s;""", (b,))
            cursor.execute("""UPDATE users SET points=%S WHERE login=%s;""", (we.points, we.login,))
            cursor.close()
            conn.close()

    #убираем этого игрока из списка игроков
    list_of_player.remove(we)

