# -*- coding:utf8 -*-

import socketserver
import threading
import connector_predict
import random


class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):

        # get socket request
        socket = self.request   #1

        # show client
        print('Connect with : ' + self.client_address[0])   #

        # set file name
        # num = random.random() * 100000
        # file_name = 'image_temp/file_' + str(int(num)) + '.jpg'

        # get image file size from client
        str = socket.recv(1024) #5
        socket.sendall("보내는 메세지 입니다".encode()) #6
        print('set file size : ' + str.decode())
        print(str.decode())
        # get image file byte stream from client
        # make empty image file
        # with open(str_size, 'wb') as image_file:
        #     data_tmp = ''
        #     while True:
        #         # save image file from client stream
        #         data = socket.recv(1024)
        #         # print(type(data))
        #         image_file.write(data)
        #         for i in data[:]:
        #             data_tmp += chr(i)
        #
        #
        #         if ((data_tmp.__len__()) * 100 == int(file_size)):
        #             # check image file size
        #             # print('received file size : {}'.format(data_tmp.__len__())*100)
        #             break

        print('received & save image : ' + str.decode())

        # tensorflow image classfication
        # connector_inst = connector_predict.Connect(file_name)
        # label = connector_inst.get_result()
        str2 = socket.recv(1024)
        print(str2.decode())
        socket.sendall("잘끝났다".encode())
        socket.close()

        
if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 5000

    server = socketserver.TCPServer((HOST, PORT), RequestHandler)

    print('Socket is now listening ...')
    server_thread = threading.Thread(target=server.serve_forever())
    server_thread.setDaemon(True)
    server_thread.start()
