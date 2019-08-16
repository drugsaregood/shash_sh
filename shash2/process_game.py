#самый сложный модуль!!!!!!!!!!!!!!проверить!


from consignment import *
from wantnewgame import *
#все что связано с анализом поля при процессе игры

#вернуть игру по токену_игры
def token_in_game(tok):
    for i in list_of_Сonsignment:
        if i.token == tok:
            return i
    return 0


#по координатам клетки определяем свободна ли она, если нет то вернем ее цвет
def free_kletk(sim,num,field):
    for i in field:
        if i.koordin_sim==sim and i.koordin_numb==num:
            return i.colour
    #свободна
    return 0


#вернем соседние горизонтальные координаты для хода
def sosedi_sim(al):
    if al=='A':
        return ['B']
    if al=='B':
        return ['A','C']
    if al=='C':
        return ['B','D']
    if al=='D':
        return ['C','E']
    if al=='E':
        return ['D','F']
    if al=='F':
        return ['E','G']
    if al=='G':
        return ['F','H']
    if al=='H':
        return ['G']


#вернем координаты клетки за местом которую бьют
def bitt(s1,n1,s2,n2):
    if s1<s2:
        s=max(sosedi_sim(s2))
    else:
        s=min(sosedi_sim(s2))
    if n1<n2:
        n=n2+1
    else:
        n=n2-1
    return [s,n]


#вернем все доступные шашки которыми может ходить щас клиент

def number_shash(token,token_game):
    res=[]
    resk=[]
    help=[]
    must_bitt = 0  # флаг тго что надо бить
    must_bittk=0
    #сперва проверяем что цвет того кто спрашивает и цвет того кто должен щас ходить совпадают
    game=token_in_game(token_game)
    if (game.must_step=='white' and game.player_white.token!=token) or (game.must_step=='black' and game.player_black.token!=token):
        #он щас не ходит
        return []
    #дальше идем и анализируем месторасположение его шашек
    for i in game.our_zoo:

        if i.colour==game.must_step:
            #если шашка интересующего нас цвета
            #сперва проверка на возможности приметивной шашки
            if must_bitt==0:#если не бьем а просто ходим
                if game.must_step=='white':
                    if i.koordin_numb>1:
                    #у белых смотрим строку меньше
                    #координаты для обследования
                        koord_sim=sosedi_sim(i.koordin_sim) #список соседних координат
                        koord_num=i.koordin_numb-1
                        for b in koord_sim:
                            if free_kletk(b,koord_num,game.our_zoo)==0:
                                res.append(i)
                                continue
                else:
                    #у черных строку больше
                    if i.koordin_numb <8:
                        # координаты для обследования
                        koord_sim = sosedi_sim(i.koordin_sim)  # список соседних координат
                        koord_num = i.koordin_numb + 1
                        for b in koord_sim:
                            if free_kletk(b, koord_num, game.our_zoo) == 0:
                                res.append(i)
                                continue
            #т к можем бить как назад так и вперед до от цвета не зависит в случае если мы бьем
            #координаты где должна стоять шашка противоположного цвета
            koord_sim = sosedi_sim(i.koordin_sim)
            koord_num = [i.koordin_numb + 1,i.koordin_numb -1]
            for g in koord_sim:
                for h in koord_num:
                    #проверяем что они не у стеночки
                    if h==8 or h==2 or g=='H' or g=='A':
                        continue
                    if free_kletk(g,h,game.our_zoo)==anti_colour(game.must_step):
                        #если это клетка противоположного цвета то проверяем если за ней пустота
                        a=bitt(i.koordin_sim,i.koordin_numb,g,h)
                        if free_kletk(a[0],a[1],game.our_zoo )==0:
                            #если там пусто то мы можем съесть
                            #если мы до этого не били то включаем этот режим и удаляем из результирующего списка преждний мусор
                            if must_bitt==0:
                                res=[]
                                must_bitt = 1
                            res.append(i)
                            continue





            if i.king==1:
                #если это дамка
                #проверяем есть ли что съесть
                koord_sim = sosedi_sim(i.koordin_sim)  # список соседних координат
                koord_num = [i.koordin_numb + 1, i.koordin_numb - 1]
                for g in koord_sim:
                    for h in koord_num:
                        # проверяем что они не у стеночки
                        if h == 8 or h == 2 or g == 'H' or g == 'A':
                            continue
                        if diagonal(i.koordin_sim,i.koordin_numb,g,h,game):
                            #если там есть штука для битья
                            must_bittk=1
                            resk.append(i)

    if must_bittk==must_bitt:
        res+=resk
    else:
        if must_bittk==1:
            res=resk
    game.can_step(res,must_bittk+must_bitt)

    return res



#анализ дамочного луча - либо доходит до его конца либо упиремтся в чужую
def diagonal(s1,n1,s2,n2,game):
    if n2 == 8 or n2 == 2 or s2 == 'H' or s2 == 'A':
        #конец
        return 0
    if free_kletk(s2, n2, game.our_zoo) == game.must_step:
        # если вплотную стоит шашка того же цвета то ничего не выйдет
        return 0
    if free_kletk(s2, n2, game.our_zoo) == anti_colour(game.must_step):
        # если там чужая фишка то нужно узнать есть ли за ней пустое место
        g = bitt(s1, n1, s2, n2)
        if free_kletk(g[0],g[1],game.our_zoo)==0:
            #если там есть пустая клетка
            return 1
        return 0
    if free_kletk(s2, n2, game.our_zoo) == 0:
        # если там пусто то идем дальше по диагонали
        g=bitt(s1,n1, s2, n2)
        return diagonal(s2,n2,g[0],g[1])
