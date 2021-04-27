import pandas as pd
import datetime
import matplotlib.pyplot as plt
# 한글등록
from matplotlib import font_manager, rc  # rc : resource

def mainre(getcategory, temp,add):
    # 추가설정 - 폰트를 변경하면 -표시가 ㅁ으로 변경되기에 '-'를 변경하지 않도록 지정
    plt.rcParams['axes.unicode_minus'] = False

    fong_loc = "c:/Windows/Fonts/malgun.ttf"  # 글꼴 경로
    font_name = font_manager.FontProperties(fname=fong_loc).get_name()
    # print(font_name) # 폰트매니저를 통해 인식하고 있는 글꼴 이름을 가져온다
    rc('font', family=font_name)  # 리소스에 글꼴을 등록

    d = datetime.datetime.today().weekday()+1
    m = datetime.datetime.today().month
    # y = datetime.datetime.today().year

    data = pd.read_csv("data/main.csv", encoding='CP949')
    yuil = data[(data["CTGG_NM"]==add)&(data["DAY_CD"]==d)&(data["MONTH"]==m)&(data["RANK"]==1)]

    # data[data["CTGG_NM"]=="송파구"]
    print(add)
    category = yuil.iloc[0,2]
    # category

    temp = float(temp)

    nalsi = ['카테고리','clear sky','few clouds','scattered clouds','broken clouds','shower rain','rain','thunderstorm','snow','mist']
    # index_col : 지정한 컬럼을 Row Index로 사용한다.
    ondo = pd.read_csv('data/mainpage.csv', encoding="euc-kr")
    ondo
    ondo.set_index(ondo['온도'],inplace=True)
    ondo
    del ondo['온도']

    categoryindex = nalsi.index(getcategory)

    if temp >= 30:
        temp = 30
    elif temp >= 25:
        temp = 30
    elif temp >= 20:
        temp = 25
    elif temp >= 15:
        temp = 20
    else:
        temp = 15

    menu = ondo[ondo['카테고리']==category].loc[[temp]].iloc[0,categoryindex]#2자리에 categoryindex

    nalsihangle = ['카테고리',"맑음",'조금 맑음','조금 구름','구름 많음','소나기','비','번개','눈','안개']

    return '{"온도":'+'"'+str(temp)+'"'+',"날씨":'+'"'+nalsihangle[categoryindex]+'"'+',"카테고리":'+'"'+category+'"'+',"메뉴":'+'"'+menu+'"'+',"주소":'+'"'+add+'"'+'}'