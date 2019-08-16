from field import  *
#все что касается сессии игры

#список всех партий текущих игры
list_of_Сonsignment=[]

#класс для непосредственно игры
#содержит двух игроков и поле
class Сonsignment:
    def __init__(self,pl1,pl2,token ):
        self.player_white=pl1
        self.player_black=pl2
        self.field=Aquarium()
        self.token=token
        self.must_step='white'
        list_of_Сonsignment.append(self)
       #добавляем доп словари из тех шашк которыми может походить игрок данного цвета
    def can_step(self, d,b):
        #признак надобности бить
        self.bitt = b
        if self.must_step=='white':
            self.can_step_white=d
        else:
            self.can_step_black=d


#вернуть соперника
def adr_opponent(we,tok_game):
    i=token_in_game(tok_game)
    if i.player_white==we:
        return i.player_black
    else:
        return i.player_white

#вернуть игру по токену игры
def token_in_game(tok):
    for i in list_of_Сonsignment:
        if i.token==tok:
            return i