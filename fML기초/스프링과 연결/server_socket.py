# -*- coding:utf8 -*-

import socketserver
import threading
import time

class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):

        # get socket request
        socket = self.request

        # show client
        print('Connect with : ' + self.client_address[0])

        # get image file size from client
        resultweather = socket.recv(1024)
        print(resultweather.decode())
        socket.sendall("보냈다!\n".encode())

        # get image file byte stream from client

        re = socket.recv(1024).decode()

        if (re == "Hello"):
           print("잘끝났다 ㅎㅎ")

        socket.close()


if __name__ == '__main__':
    HOST = '192.168.0.10'
    PORT = 5000

    server = socketserver.TCPServer((HOST, PORT), RequestHandler)

    print('Socket is now listening ...')
    server_thread = threading.Thread(target=server.serve_forever())
    server_thread.setDaemon(True)
    server_thread.start()