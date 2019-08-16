from player import  *
import random
from consignment import *
#все что касается новой игры и поиска партнера

#клиент хочет новую игру
def new_game(date):
    #он переходит в состояние 1 и ему вернем словарь с игроками в том же состоянии {логиин; цвет...}
    i=token_in_play(date['token'])
    if i:
        i.want_game(date['colour'])
    return {a.login : a.colour for a in list_of_player if a.state==1}

#вернуть игрока по имени
def name_in_play(name):
    for i in list_of_player:
        if i.login==name:
            return i
    return 0


#вернуть игрока по токену
def token_in_play(tok):
    for i in list_of_player:
        if i.token == tok:
            return i
    return 0

def anti_colour(colour):
    if colour=='black':
        return 'white'
    return 'black'

#создание новой партии
#цвета распределяем по тому как хочет первый
#если у второго были другие предпочтения то изменить у него их
def new_consignment(we,opp):
    #создаем токен партии
    tok = int(random.uniform(0, 1000000))
    while tok in [i.token for i in list_of_Сonsignment]:
        tok = int(random.uniform(0, 1000000))

    #распределение по цветам
    if we.colour=='white':
        Aquarium(we, opp, tok)
        opp.colour='black'
    else:
        Aquarium(opp, we, tok)
        opp.colour = 'white'
    return tok

