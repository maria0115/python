import time
import urllib
from urllib.request import urlopen
import nltk
from konlpy.tag import Okt
from bs4 import BeautifulSoup
from tqdm import tqdm_notebook
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import matplotlib

def wordcloudsearch(keyword):
    html = 'https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query={key_word}&sm=tab_pge&srchby=all&st=sim&where=post&start={num}'
    response = urlopen(html.format(num=1, key_word=urllib.parse.quote('한식')))

    soup = BeautifulSoup(response, "html.parser")

    tmp = soup.find_all('div')
    tmp_list = []
    for line in tmp:
        tmp_list.append(line.text)
    present_candi_text = []

    for n in tqdm_notebook(range(1, 100, 10)):
        response = urlopen(html.format(num=n, key_word=urllib.parse.quote('한식 메뉴')))
        soup = BeautifulSoup(response, "html.parser")
        tmp = soup.find_all('dl')

        for line in tmp:
            present_candi_text.append(line.text)
        time.sleep(1)
    okt = Okt()

    present_text = ''
    for each_line in present_candi_text[:100]:
        present_text = present_text + each_line + "\n"
    tokens_ko = okt.morphs(present_text)
    ko = nltk.Text(tokens_ko, name='한식 메뉴')
    # 의미없는 단어들을 수동으로 제거해준다.
    stop_words = ['.','가','요','답변','...','을','수','에','질문','제','를','이','도',
                          '좋','1','는','로','으로','2','것','은','다',',','니다','대','들',
                          '2017','들','데','..','의','때','겠','고','게','네요','한','일','할',
                          '10','?','하는','06','주','려고','인데','거','좀','는데','~','ㅎㅎ',
                          '하나','이상','20','뭐','까','있는','잘','습니다','다면','했','주려',
                          '지','있','못','후','중','줄','6','과','어떤','기본','!!',
                          '단어','선물해','라고','중요한','합','가요','....','보이','네','무지','블로그','입력','검색']

    tokens_ko = [each_word for each_word in tokens_ko
                              if each_word not in stop_words]

    ko = nltk.Text(tokens_ko, name='한식 메뉴')

    data = ko.vocab().most_common(100)

    matplotlib.rcParams['font.family'] = "Maulgun Gothic"
    font_path = "c:/Windows/Fonts/malgun.ttf"

    # denne_mask = np.array(Image.open('cloud.png'))
    custom_mask = np.array (Image.open ( "images.png"))
    wc = WordCloud(font_path=font_path,mask=custom_mask, background_color="white", width=800, height=600)
    cloud = wc.generate_from_frequencies(dict(data))
    plt.figure(figsize = (20, 16))
    plt.axis('off')
    plt.imshow(cloud)
    plt.savefig('./file/wordcloud.png')