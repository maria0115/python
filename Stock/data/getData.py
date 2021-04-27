import pandas as pd
import requests
"""
전체 종목코드 가져오기
"""
# 종목 타입에 따라 download url이 다름. 종목코드 뒤에 .KS .KQ등이 입력되어야해서 Download Link 구분 필요
stock_type = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt'
}

# 회사명으로 주식 종목 코드를 획득할 수 있도록 하는 함수
def get_code(df, name):
    code = df.query("name=='{}'".format(name))['code'].to_string(index=False)
    # 위와같이 code명을 가져오면 앞에 공백이 붙어있는 상황이 발생하여 앞뒤로 sript() 하여 공백 제거
    code = code.strip()
    return code

# download url 조합
def get_download_stock(market_type=None):
    market_type = stock_type[market_type]
    download_link = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    download_link = download_link + '?method=download'
    download_link = download_link + '&marketType=' + market_type

    try:
        df = pd.read_html(download_link, header=0)[0]
        return df;
    except:
        print("카카오톡 알림으로 예은이한테 종목코드 가져오기 오류났다고 알려주세요")
        print("프로그램 중지할지 실행시키고 있을지 고민고민")

# kospi 종목코드 목록 다운로드
def get_download_kospi():
    df = get_download_stock('kospi')
    df.종목코드 = df.종목코드.map('{:06d}.KS'.format)
    return df

# kosdaq 종목코드 목록 다운로드
def get_download_kosdaq():
    df = get_download_stock('kosdaq')
    df.종목코드 = df.종목코드.map('{:06d}.KQ'.format)
    return df


"""
일정기간 주식 시세
"""

import pandas_datareader as pdr

def get_date_data(code="035420.KS"):
    df = pdr.get_data_yahoo(code)
    return df


"""
년도별, 분기별 재무재표(잘 안쓸듯)
"""
def get_financial(code="A005930"):
    price_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1'
    params = {'query': code}
    price = requests.get(price_url, params=params)
    d = pd.read_html(price.text)
    data = d[10]
    data.set_index(('IFRS(연결)', 'IFRS(연결)'), inplace=True)
    data.index.rename('ifrf', inplace=True)
    yearfin = data.loc[:, 'Annual'].iloc[:, :-1]
    seasonfin = data.loc[:, 'Net Quarter'].iloc[:, :-1]
    result = {"yearfin":yearfin,"seasonfin":seasonfin}
    return result

"""
배당 포함 재무재표
"""
def get_allocation(code="005930"):
    url = 'https://finance.naver.com/item/main.nhn?code='+code
    tables = pd.read_html(url,encoding='euc-kr')
    df = tables[3]
    df.set_index(('주요재무정보', '주요재무정보', '주요재무정보'), inplace=True)
    df.index.rename('주요재무정보', inplace=True)
    df.columns = df.columns.droplevel(2)
    yearfin = df['최근 연간 실적']
    seasonfin = df['최근 분기 실적']
    result = {"yearfin": yearfin, "seasonfin": seasonfin}
    return result

"""
실시간 시세
"""
def get_realtime(code="000040"):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup

    url = "http://asp1.krx.co.kr/servlet/krx.asp.XMLSiseEng?code="+code
    req = urlopen(url)
    result = req.read()
    xmlsoup = BeautifulSoup(result, "lxml-xml")
    stock = xmlsoup.find("TBL_StockInfo")
    stock_df = pd.DataFrame(stock.attrs, index=[0])
    stock_df = stock_df.applymap(lambda x: x.replace(",", ""))

    return stock_df

"""
발행주식수
"""
def get_stockcount(code="A005930"):
    price_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1'
    params = {'query': code}
    price = requests.get(price_url, params=params)
    d = pd.read_html(price.text)[0].loc[6, 1]
    return int(d.split('/')[0].replace(" ", "").replace(",", ""))
