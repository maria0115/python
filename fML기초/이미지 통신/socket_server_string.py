# -*- coding:utf8 -*-
from tkinter import Image

import recommendations
import socketserver
import threading
import mainrecommend as main
import cx_Oracle as oci
import otherrecommand
import random
import imagetest
import os
import io
import PIL.Image as Image
from array import array
import Wordcloud
import base64

class RequestHandler(socketserver.StreamRequestHandler):
    ipcount=0



    def handle(self):
        # get socket request
        socket = self.request   #1

        # show client
        print('Connect with : ' + self.client_address[0])   #

        # get temp from client
        getwhat = socket.recv(1024)
        print('getwhat : ' + getwhat.decode())
        socket.sendall("getwhatok".encode())
        weahterThunderstorm = ["thunderstorm with light rain","thunderstorm with rain","thunderstorm with heavy rain","light thunderstorm","thunderstorm","heavy thunderstorm","ragged thunderstorm","thunderstorm with light drizzle","thunderstorm with drizzle","thunderstorm with heavy drizzle"]
        weatherDrizzle=["light intensity drizzle","drizzle","heavy intensity drizzle","light intensity drizzle rain","drizzle rain","heavy intensity drizzle rain","shower rain and drizzle","heavy shower rain and drizzle","heavy shower rain and drizzle","shower drizzle"]
        weahterRain=["light rain","moderate rain","heavy intensity rain","very heavy rain","extreme rain","freezing rain","light intensity shower rain","shower rain","heavy intensity shower rain","ragged shower rain"]
        weatherSnow=["light snow","Snow","Heavy snow","Sleet","Light shower sleet","Shower sleet","Light rain and snow","Rain and snow","Light shower snow","Shower snow","Heavy shower snow"]
        weatherAtmosphere=["haze","mist","Smoke","Haze","sand/ dust whirls","fog","sand","dust","volcanic ash","squalls","tornado"]
        weatherClear=["clear sky"]
        weatherClouds=["few clouds","scattered clouds","broken clouds","overcast clouds"]

        if getwhat.decode()=='main':
            ip = socket.recv(1024)
            print('ipok : ' + ip.decode())
            socket.sendall(self.client_address[0].encode())
            weather = socket.recv(1024)
            print('weather : ' + weather.decode())
            socket.sendall("weatherok".encode())
            weather = weather.decode()
            if weather in weahterThunderstorm:
                weather="thunderstorm"
            elif weather in weatherAtmosphere:
                weather="mist"
            elif weather in weatherSnow:
                weather="snow"
            elif weather in weatherClear:
                weather="clear sky"
            elif weather in weahterRain:
                weather="rain"
            elif weather in weatherDrizzle:
                weather="shower rain"
            elif weather=="overcast clouds":
                weather="broken clouds"
            print(weather)

            temp = socket.recv(1024) #5
            print('temp : ' + temp.decode())
            socket.sendall("tempok".encode())  # 6

            add = socket.recv(1024)  # 5
            print('add : ' + add.decode())
            socket.sendall("addok".encode())  # 6

            resultr = socket.recv(1024)
            print('resultr : ' + resultr.decode())

            temp = temp.decode()
            add = add.decode()
            result = main.mainre(weather,temp,add)
            print(result)
            socket.sendall(result.encode())
        elif getwhat.decode()=='other':
            me = socket.recv(1024).decode()  # 5

            print('me : ' + me)
            resultone = otherrecommand.select_one_most(me)
            print(resultone)

            otherdic = {}
            resultmost = otherrecommand.select_other_most()
            print("resultmost : ",resultmost)

            mlist = ()
            mlist = ('hihi',)
            mlist = mlist + ('hi',)
            mlist

            for id, most in resultmost:
                if most is not None:
                    hi = most.split(",")

                    onedic={}
                    for m,i in enumerate(hi):
                        onedic[i] = m
                        mlist = mlist + (i,)
                    otherdic[id]=onedic
            print(otherdic)
            resultorder = otherrecommand.select_other_order(mlist)
            print(resultorder)
            for i in resultorder:
                otherdic[i[2]][i[1]] = i[0]
                print(otherdic[i[2]])

            oth = ""
            for score, other in recommendations.top_matches(otherdic, me):
                print("me and", other, score)
                oth=oth+","+other
            print(oth,"****************")

            socket.sendall(oth.encode())
        elif getwhat.decode() == 'image':
            # set file name
            num = random.random() * 100000
            file_name = 'image_temp/file_' + str(int(num)) + '.jpg'

            # get image file size from client
            file_size = socket.recv(1024)  # 2
            socket.sendall(file_size)  # 3
            print('set file size : ' + str(file_size))
            print(int(file_size))
            # get image file byte stream from client
            # make empty image file
            result =""
            data_tmp = ''
            print(file_name)

            filena = open(file_name, 'wb')
            while True:
                # save image file from client stream
                data = socket.recv(1024)  # 6
                if not data:
                    break
                filena.write(data)
                print(data)

                for i in data[:]:
                    data_tmp += chr(i)

                if ((data_tmp.__len__()) * 100 == int(file_size)):
                    # check image file size
                    # print('received file size : {}'.format(data_tmp.__len__())*100)

                    result = imagetest.check_photo_str(file_name)
                    print(result)
                    break

            filena.close()
            print('received & save image : ' + result)
            socket.sendall(result.encode())
        elif getwhat.decode() == 'wordcloud':
            searchkeyword = socket.recv(1024)  # 5
            print('searchkeyword : ' + searchkeyword.decode())
            socket.sendall("searchkeywordok".encode())  # 6
            searchkeyword = searchkeyword.decode()

            # 여기서 워드클라우드 돌리기
            Wordcloud.wordcloudsearch(searchkeyword)

            file = './file/wordcloud.png'
            fileSize = os.path.getsize(file)
            print(str(fileSize))
            #
            # conn.sendall(fileSize.encode())
            reReady = socket.recv(1024)
            print('reReady : ' + reReady.decode())
            if reReady.decode() == "reReady":
                resize = str(fileSize)
                socket.sendall(resize.encode())

            filereReady = socket.recv(1024)
            print('filereReady : ' + filereReady.decode())
            socket.sendall("filereReady".encode())
            if filereReady.decode() == "filereReady":
                with open(file, "rb") as imageFile:
                    str_ = base64.b64encode(imageFile.read())
                    print(str_)
                    print(len(str_))

                    filesizeok = socket.recv(1024)
                    print('filesizeok : ' + filesizeok.decode())
                    socket.sendall(str(len(str_)).encode())

                    fileok = socket.recv(1024)
                    print('fileok : ' + fileok.decode())
                    socket.sendall(str_)


        socket.close()




        
if __name__ == '__main__':
    HOST = '192.168.0.10'
    PORT = 5000


    server = socketserver.TCPServer((HOST, PORT), RequestHandler)

    print('Socket is now listening ...')
    server_thread = threading.Thread(target=server.serve_forever())
    server_thread.setDaemon(True)
    server_thread.start()
