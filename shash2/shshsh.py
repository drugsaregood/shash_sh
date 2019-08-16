#модуль подключения и отправки данных в формате json
import socket
import socketserver
import threading
import time
#import for_result
from for_result import *


def from_js(date):
    pass


def in_js(date):
    pass



#обработчик запросов
class TCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        #инфа что мы получили
        date=from_js(self.request.recv(1024))
        #получаем результат обработки запроса в виде словаря
        answer=result(date,self.client_address)
        #дальше идем по этому словарю где ключом является адрес тому кому слать а значением что слать
        #{('ip', №_port): объект_для_отправки, ...}
        for i in answer:
            sock = socket.socket()
            sock.connect(i[0],i[1])
            sock.send(in_js(answer[i]))
            sock.close()










class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass



if __name__ == "__main__":
    #адрес и порт нашего сервера
    HOST, PORT = "localhost", 9001
    server = ThreadedTCPServer((HOST, PORT), TCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = False
    server_thread.start()
#чтобы сервер закрылся только при исключении, например прерывании с клавиатуры
    while True:
        try:
            print(time.time())
            time.sleep(1)
        except:
            break

    server.shutdown()
    server.server_close()

