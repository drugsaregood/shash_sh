from registration import *
from wantnewgame import  *
from process_game import *
from wantend import *

#функция непосредственной обработки пришедшего результата и формирования ответа
# {('ip', №_port): объект_для_отправки, ...}


def result(date, client_adr):

    #регистрация
    if date['code']==0:
       if ckeck_in(date['login'], date['password']):
           return {(client_adr[0],client_adr[1]):{'code':0,'remark':'ok'}}
       else:
           return {(client_adr[0],client_adr[1]):{'code':1,'remark':'name is busy already'}}

    #авторизация
    if date['code']==1:
        bo, tok= authoriz(date['login'], date['password'],client_adr)
        if bo==1:
            #норм
            return {(client_adr[0], client_adr[1]): {'code': 0, 'remark': 'ok', 'token': tok}}
        if bo==0:
            #неверный пароль
            return {(client_adr[0], client_adr[1]): {'code': 2, 'remark': 'error password'}}
        if bo==2:
            #зашел уже с другого хоста
            return {(client_adr[0], client_adr[1]): {'code': 2, 'remark': 'you are already logged in from another device'}}

    #новая игра
    if date['code']==2:
        return {(client_adr[0], client_adr[1]): {'code': 0, 'remark': '', 'list_plays':new_game(date)}}

    #запрос/ответ взять участника в соперники
    if date['code']==3:

        if date['type']=='reques':
            #если это предложение поиграть
            # по имени определяем игрока для отправки
            opp = name_in_play(date['name'])
            we= token_in_play(date['token'])
            return {(opp.ip, opp.port):{'code': 3, 'remark': '','namw':we.login, 'points':we.points }}
        if date['type']=='response':
            #если это ответ на предлжение поиграть
            opp=name_in_play(date['name'])
            we = token_in_play(date['token'])
            if date['solve']=='yes':
                #мы согласны играть
                #находим токен для нашей игры, регистрируем партию
                tok_game=new_consignment(we,opp)
                return {(we.ip, we.port):{'code': 4, 'remark': 'Yes play', 'token_game':tok_game, 'colour':we.colour}, (opp.ip, opp.port):{'code': 4, 'remark': 'Yes play', 'token_game':tok_game, 'colour':anti_colour(we.colour)}}
            else:
                #мы не хотим играть
                return {(opp.ip, opp.port):{'code': 5, 'remark': 'Not play'}}



    #вопрос о номерах шашек которыми может ходить клиент
    if date['code']==4:
        return {'code':0, 'remark':'', 'number_shash':number_shash(date['token'],date['token_game']) }

    #чтобы не отвалиться по таймауту для таймаута!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if date['code']==5:
        pass

    # запрос/ответ о ничьей
    if date['code']==6:
        opp = adr_opponent(date['token'], date['token_game'])
        if date['type'] == 'reques':
            #если это предложение о ничьей
            #определяем адрес соперника

            return {(opp.ip, opp.port):{'code': 6, 'remark': 'eqvialy' }}
        else:
            #ответ на ничью
            if date['solve']=='yes':
                #согласны на ничью
                we=token_in_play(date['token'])
                are_equal(date['token_game'])
                return {(we.ip, we.port):{'code': 10, 'remark': 'eqial'}, (opp.ip, opp.port):{'code': 10, 'remark': 'eqial'}}
            else:
                #не согласны на ничью
                return {(opp.ip, opp.port):{'code': 7, 'remark': 'failure' }}


    #сдаться
    if date['code']==7:
        opp = adr_opponent(date['token'], date['token_game'])
        we = token_in_play(date['token'])
        give_up(date['token_game'],date['token'])
        return {(we.ip, we.port):{'code': 9, 'remark': 'not win'}, (opp.ip, opp.port):{'code': 8, 'remark': 'win'}}
    #ход!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if date['code']==8:
        we = token_in_play(date['token'])
        #функция определяем можем ли мы так ходить 1-можно так, 0-нельзя
        if analis_step(date['token'], date['token_game'], date['protokol']):
            #делаем этот ход
            opp = adr_opponent(date['token'], date['token_game'])
            v=do_step(date['token'], date['token_game'], date['protokol'])  #[код результата 1, объект-поле]
            opp = adr_opponent(date['token'], date['token_game'])
            #анализируем никто ли тут не победил
            if v[0]==0:
                #если пока никто не выйграл то пересылаем результат поля
                return {(we.ip, we.port): {'code': 0, 'remark': 'ok', 'field':v[1]}, (opp.ip, opp.port): {'code': 10, 'remark': 'eqial', 'field':v[1]}}

            # тут также у нас долна закончится партия и сформироваться баллы
            if v[0] == 1:
            # если он выйграл
                return {(we.ip, we.port): {'code': 8, 'remark': 'win'}, (opp.ip, opp.port): {'code': 9, 'remark': 'not win'}}

            if v[0]==2:
            # если он проиграл
                return {(we.ip, we.port): {'code': 9, 'remark': 'not win'}, (opp.ip, opp.port): {'code': 8, 'remark': 'win'}}

        else:
            #если так ходить нельзя
            return  {(we.ip, we.port):{'code': 11, 'remark': 'error step' }}



    #закрыть приложение(такая возможность есть только у клиента в состоянии 0
    if date['code']==9:
        exit_ap(date['token'])
        we = token_in_play(date['token'])
        return {(we.ip, we.port):{'code': 0, 'remark': 'ok'}}