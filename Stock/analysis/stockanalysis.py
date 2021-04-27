import os
import sys
from data.getData import *
class Analysis():
    def __init__(self):
        super().__init__()


        self.yearcondition = {'c1': False, 'c2': False, 'c3': False, 'c4': False, 'c5': False, 'c6': False, 'c7': False,
                              'c8': False, 'c9': False, 'c10': False, 'c11': False}
        self.seasoncondition = {'c1': False, 'c2': False, 'c3': False, 'c4': False, 'c5': False, 'c6': False,
                                'c7': False,
                                'c8': False, 'c9': False, 'c10': False, 'c11': False}
        self.messages = {'c1': '', 'c2': '', 'c3': '', 'c4': '', 'c5': '', 'c6': '', 'c7': '', 'c8': '', 'c9': '',
                         'c10': '',
                         'c11': ''}


        """
        전체 종목코드 가져오기
        """

        stockcode_kospi = get_download_kospi()
        stockcode_kosdaq = get_download_kosdaq()
        self.stockcode = pd.concat([stockcode_kospi, stockcode_kosdaq])

