import socket
import socketserver
import threading
import time
import re


#класс клетка в котором может находиться шашка
class Kletka():
    def __init__(self,c):
        self.Colour = c
        #является ли клетка носителем дамки
        self.king = false

    def serialize(self):
        return json.dumps(self.__dict__)
    @classmethod
    def deserialize(cls,date):
        z=json.loads(date)
        c=Kletka(z['Colour'])
        c.king=z['king']
        return c



#класс поле
class Field():
    #такого поле при создании новой игры
    def __init__(self):
        f=[]
        for j in range(8):
            l = []
            for i in range(4):
                if j in [0, 1, 2]:
                    l.append(Kletka('black'))
                if j in [3, 4]:
                    l.append(Kletka('zero'))
                if j in [5, 6, 7]:
                    l.append(Kletka('white'))
            f.append(l)
        self.f=f

    def serialize(self):
        l = []
        for i in self.f:
            h = []
            for j in i:
                h.append(j.serialize())
            l.append(json.dumps(h))
        return json.dumps(l)

    @classmethod
    def deserialize(cls, date):
        l = json.loads(date)
        res = []
        for i in l:
            help = json.loads(i)
            h = []
            for j in help:
                h.append(Kletka.deserialize(j))
            res.append(h)
        return res





class Player:
    def __init__(self, id, name, client_adress,client_port):
        #адрес клиента
        self.ip = client_adress
        self.port = client_port
        self.id = id
        self.name = name
        #состояние 1 - прошел авторизацию но еще не играет, состояние 2 - еще не играет и ждет появление партнера по игре, состояние 3 - в игре
        self.state=1
        #и автоматом кидаем его в наш список игроков
        list_of_player.append(self)


#класс для непосредственно игры
#содержит двух игроков и поле
class Сonsignment:
    def __init__(self,pl1,pl2,id ):
        self.player_white=pl1
        self.player_black=pl2
        self.field=Field()
        self.id=id
        self.must_step='white'
        list_of_Сonsignment.append(self)
# функция проверяет можно ли так походить
#date[1] - id клиента
#date{2} - id партии
#date[3] -  объект поле где изменено положение некоторых шашек
#вернем список [ответ_да/нет , комментарий(если нет)]
def can_step(date):
    pass


#функция выводит результирующее объект поле (в отличие от того что пришло там могут быть убраны съеденные соперником шашки) также все запоминается в текущей партии игры
#в случае победы/проигрыша формирует эти сообщения
#результат список [поле филд, поле филд ] или [3,4] / [4,3]
def res_field(date):
    pass

#список всех авторизированных игроков
list_of_player=[]


#список всех текущих партий
list_of_Сonsignment=[]


#формирует адрес соперника(адрес и порт)
def opponent_adr(client_id):
    t=0
    for i in list_of_Сonsignment:
        if i.player_white.id==client_id:
            t=i.player_black.id
            break
        if i.player_black.id==client_id:
            t=i.player_white.id
            break
    for i in list_of_player:
        if i.id==t:
            return[i.ip, i.port]


#функция формирует список - первый аргумент результат для посылающего, второй - для его соперника
#коды входящих сообщений
#0 - авторизация
#1 - новая игра
#2 - закрыть текущую партию
#3 - ход в игре
#4 - закрыть все приложение
def result(date, client_adress):
    #авторизация
    #ответ только клиенту
    if date[0]==0:
        #вторым параметром тут идем имя клиента
        #надо проверить что игроков с таким именем нет. если есть то вернуть список с ошибкой 1 - имя занято
        if date[1] in [i.name for i in list_of_player]:
            return [1]
        #подбираем ему id:
        if len(list_of_player)==0:
            id=0
        else:
            id==max([i.id for i in list_of_player])+1
        Player(id, date[1], client_adress[0], client_adress[1])
        return [0, id]

    #новая игра
    #в случае если свободных клиентов нет - ответ клиенту с сообщением подожать через 8 секунд
    #если соперник есть - ответ и тому и другому о начале сессии
    if date[0]==1:
        #меняем статус учасника на состояние 2
        cl=0
        for i in list_of_player:
            if i.id==date[1]:
                cl=i
                i.state=2
                break
        #ставим таймер
        begin_time=time.time()
        #если 8 с не прошло ты мы остаемся в поиске
        #!!!!!!!!!!!!!!!!! а не нужно ли если найти соперника ставить на него блокировку пока он не нашел другого соперника?????????????????????????????
        while time.time()-begin_time<8:
            for i in list_of_player:
                if i.id!=date[1] and i.state==2:
                # если нашли партнера то нам и ему пишем сообщение и переводим их в состояние3 и создаем партию
                    i.state=3
                    cl.state=3
                    # подбираем id для партии:
                    if len(list_of_Сonsignment) == 0:
                        id = 0
                    else:
                        id == max([i.id for i in list_of_Сonsignment]) + 1
                    Сonsignment(cl,i,id)

                    return [[0,id, 'white'],[0,id,'black']]
            time.sleep(1)
         # иначе шлем клиенту ошибку с кодом 1(нет свободного противника)
        return [1]



    #2-закрыть текущую партию
    #письмо двум участникам
    #тому кто попросил говорим что он проиграл а его сопернику что он выйграл
    if date[0]==2:
        return [[0,4],[0,3]]





    #ход в игре
    #если так походить можно - сообщение и ему и сопернику
    #если нельзя - только ему с названием ошибки
    if date[0]==3:
        #проверяем можно ли так ходить
        r=can_step(date)
        if r[0]:
            #если так походить можно
            x=res_field(date)
            return [[0, x[0]],[0,x[1]]]
        #если так ходить нельзя шлем код 5 и комментарий клиенту
        return [5, r[1]]






    # 4-закрыть приложение
    # если он играет - письмо двум участникам
    # если не играет - только клиенту
    if date[0]==4:
        #сперва определим состояние клиента
        for i in list_of_player:
            if i.id==date[1]:
                if i.state==3:
                    #если клиент играет
                    return [[0,4],[0,3]]
                return [0]

#десеарилизация объекта(из потока байт в объект)
def from_js(date):
    h=json.loads(date)
    res=[]
    for i in h:
        #для проверки это обычный аргумент или поле, оно в json начинается с [
        l=re.findall(r'.', str(i))[0]
        if l!='[':
            res.append(i)
        else:
            res.append(Field.deserialize(i))
    return res

#сериализация объекта(из объекта в поток байт)
def in_js(date):
    h=[]
    for i in date:
        if isinstance(i, Field):
            i=i.serialize()
        h.append(i)
    return json.dumps(h)

#обработчик запросов
class TCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        encoding = "utf-8"
        #инфа что мы получили
        data = self.request.recv(1024)
        # Дальше мы обрабатываем данные, которые пришли
        #т к мы передаем наши данные в формате джейсон то нам надо его сперва конвектировать из байт а при отправке наоборот
        date=from_js(date)
        answer=result(date,self.client_address)
        #ответ для того кто прислал
        self.request.send(in_js(answer[0]))
        #если есть еще ответ для соперника то отослать ему его
        if len(answer)>1:
            sock = socket.socket()
            opponent=opponent_adr(date[1])
            sock.connect((opponent[0], opponent_adr([1])))
            sock.send(in_js(answer[1]))
            sock.close()






class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass



if __name__ == "__main__":
    #адрес и порт нашего сервера
    HOST, PORT = "localhost", 9000
    server = ThreadedTCPServer((HOST, PORT), TCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = False
    server_thread.start()
#чтобы сервер закрылся только при исключении, например прерывании с клавиатуры
    while True:
        try:
            time.sleep(1)
        except:
            break

    server.shutdown()
    server.server_close()

