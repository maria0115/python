import osimport sysfrom PyQt5.QAxContainer import *    #키움증권 api를 제어할 수 있도록from PyQt5.QtCore import *from PyQt5.QtTest import *from config.errorcode import *from config.kiwoomType import *from config.log_class import *class Kiwoom(QAxWidget):    def __init__(self):        super().__init__()  #QAxWidget의 함수들을 상속받아 사용하기 위해        self.realType = RealType()        # self.logging = Logging()        # self.slack = Slack() #슬랙 동작        # self.logging.logger.debug("Kiwoom() class start.")        ###############변수모음        self.account_num = None        ####################################        ####### 요청 스크린 번호        self.screen_my_info = "2000"  # 계좌 관련한 스크린 번호        self.screen_calculation_stock = "4000"  # 계산용 스크린 번호        self.screen_real_stock = "5000"  # 종목별 할당할 스크린 번호        self.screen_meme_stock = "6000"  # 종목별 할당할 주문용스크린 번호        self.screen_start_stop_real = "1000"  # 장 시작/종료 실시간 스크린번호        ########################################        ####### event loop를 실행하기 위한 변수모음        self.login_event_loop = QEventLoop()  # 로그인 요청용 이벤트루프        self.detail_account_info_event_loop = QEventLoop()  # 예수금 요청용 이벤트루프        self.calculator_event_loop = QEventLoop()        #########################################        ######## 종목 정보 가져오기        self.portfolio_stock_dict = {}        self.jango_dict = {}        ########################        ########### 종목 분석 용        self.calcul_data = []        ##########################################        ################계좌관련 변수모음음        self.use_money_percent = 0.5        self.use_money = 0        ########### 전체 종목 관리        self.all_stock_dict = {}        ###########################        ####### 계좌 관련된 변수        self.account_stock_dict = {}        self.not_account_stock_dict = {}        self.deposit = 0  # 예수금        self.use_money = 0  # 실제 투자에 사용할 금액        self.use_money_percent = 0.5  # 예수금에서 실제 사용할 비율        self.output_deposit = 0  # 출력가능 금액        self.total_profit_loss_money = 0  # 총평가손익금액        self.total_profit_loss_rate = 0.0  # 총수익률(%)        ########################################        ######### 초기 셋팅 함수들 바로 실행        self.get_ocx_instance()  # OCX 방식을 파이썬에 사용할 수 있게 변환해 주는 함수        self.event_slots()  # 키움과 연결하기 위한 시그널 / 슬롯 모음        self.real_event_slot()  # 실시간 이벤트 시그널 / 슬롯 연결        self.signal_login_CommConnect()  # 로그인 요청 시그널 포함        self.get_account_info()  # 계좌번호 가져오기        self.detail_account_info()  # 예수금 요청 시그널 포함        self.detail_account_mystock()  # 계좌평가잔고내역 요청 시그널 포함        QTimer.singleShot(5000, self.not_concluded_account)  # 5초 뒤에 미체결 종목들 가져오기 실행        #########################################        # self.calculator_fnc() # 종목 분석용, 임시용으로 실행        QTest.qWait(10000)        self.read_code() # 저장된 종목들 불러온다.        self.screen_number_setting() # 스크린번호를 할당        QTest.qWait(5000)        # 실시간 수신 관련 함수        self.dynamicCall("SetRealReg(QString,QString,QString,QString)",self.screen_start_stop_real,"",self.realType.REALTYPE['장시작시간']['장운영구분'],"0")        for code in self.portfolio_stock_dict.keys():            screen_num = self.portfolio_stock_dict[code]["스크린번호"]            fids = self.realType.REALTYPE['주식체결']['체결시간']            self.dynamicCall("SetRealReg(QString,QString,QString,QString)", screen_num, code,fids, "1")            print("실시간 등록 코드 : %s, 스크린번호 : %s, fid번호 : %s"%(code,screen_num,fids))    def get_ocx_instance(self):             # 키움API를 python에서 사용할 수 있게끔 만들어줌        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')    #응용프로그램을 제어할 수 있도록 만들어줌(경로설정)        print("ocx")    def event_slots(self):                   # 로그인상태 전달        print("1 일단 로그인 상태를 알기 위한 함수를 메모리에 올림")        self.OnEventConnect.connect(self.login_slot)    #로그인처리이벤트.connect(에러코드 던져즐곳)        print("2 로그인처리가 되면 login_slot함수에 return값 보내줌")        # print("event")        self.OnReceiveTrData.connect(self.trdata_slot)    def real_event_slot(self):        self.OnReceiveRealData.connect(self.realdata_slot)        self.OnReceiveChejanData.connect(self.chejan_slot)    def login_slot(self,errCode):        # print("login")        print("7")        print(errors(errCode))        print("8")        self.login_event_loop.exit()        print("9")    def signal_login_CommConnect(self):     # 수동 로그인설정인 경우 로그인창을 출력.                                            # 자동로그인 설정인 경우 로그인창에서 자동으로 로그인을 시도합니다.        print("3 로그인창 띄우는 함수")        self.dynamicCall('CommConnect()')   #network적이거나 다른서버응용프로그램에 데이터를 전송할 수 있게끔(전달할함수)        print("4")        # print("signal")        #로그인을 요청했는데 로그인 반환을 아직 안한 상태에서 login_slot을 요청했기 때문에        print("5")        self.login_event_loop.exec_()           #다음게 실행하지 않도록 막음        print("6")    def get_account_info(self):        account_list = self.dynamicCall("GetLogininfo(String)","ACCNO")        self.account_num = account_list.split(';')[0]        print("나의 보유 계좌번호 %s"%self.account_num)    def detail_account_info(self):        print("예수금 요청하는 부분")        # self.dynamicCall("계좌번호","8159959711")        self.dynamicCall("SetInputValue(QString,QString)","계좌번호",self.account_num)        self.dynamicCall("SetInputValue(QString,QString)", "비밀번호", "0000")        self.dynamicCall("SetInputValue(QString,QString)", "비밀번호입력매체구분", "00")        self.dynamicCall("SetInputValue(QString,QString)", "조회구분", "2")        self.dynamicCall("CommRqData(QString,QString,int,QString)","예수금상세현황요청","opw00001","0",self.screen_my_info)        print("예수금 이벤트루프 실행")        self.detail_account_info_event_loop.exec_()    def detail_account_mystock(self,sPrevNext="0"):        print("계좌평가 잔고내역 요청")        self.dynamicCall("SetInputValue(QString,QString)", "계좌번호", self.account_num)        self.dynamicCall("SetInputValue(QString,QString)", "비밀번호", "0000")        self.dynamicCall("SetInputValue(QString,QString)", "비밀번호입력매체구분", "00")        self.dynamicCall("SetInputValue(QString,QString)", "조회구분", "2")        self.dynamicCall("CommRqData(QString,QString,int,QString)", "계좌평가잔고내역", "opw00018", sPrevNext, self.screen_my_info)        if sPrevNext == "0" or sPrevNext == "":            print("계좌평가 잔고내역 요청 이벤트 루프 시작")            self.detail_account_info_event_loop.exec_()    def not_concluded_account(self, sPrevNext="0"):        print("미체결 요청")        self.dynamicCall("SetInputValue(QString,QString)", "계좌번호", self.account_num)        self.dynamicCall("SetInputValue(QString,QString)", "체결구분","1")        self.dynamicCall("SetInputValue(QString,QString)", "매매구분","0")        self.dynamicCall("CommRqData(QString,QString,int,QString)", "실시간미체결요청", "opt10075", sPrevNext, self.screen_my_info)        print("미체결 이벤트루프 실행")        self.detail_account_info_event_loop.exec_()        # SetInputValue("매매구분","")    def trdata_slot(self, sScrNo, sRQName,sTrCode,sRecordName,sPrevNext):        '''        tr요청을 받는 구역이다! 슬롯이다!        :param sScrNo: 스크린번호        :param sRQName: 내가 요청했을 때 지은 이름        :param sTrCode: 요청 id, tr코드        :param sRecordName: 사용안함        :param sPrevNext: 다음페이지가 있는지        :return:        '''        if sRQName == "예수금상세현황요청":            deposit = self.dynamicCall("GetCommData(QString,QString,int,QString)",sTrCode,sRQName,0,"예수금")            print("예수금 %s"%deposit)            self.use_money = int(deposit)*self.use_money_percent            self.use_money = self.use_money / 4     #다 안사도록 재코딩            ok_deposit = self.dynamicCall("GetCommData(QString,QString,int,QString",sTrCode,sRQName,0,"출금가능금액")            print("출금가능금액 %s"%ok_deposit)            ok_depositresult = int(ok_deposit)            print("예수금상세현황요청 이벤트루프 종료")            self.detail_account_info_event_loop.exit()        elif sRQName =="계좌평가잔고내역":            total_buy_money = self.dynamicCall("GetCommData(QString,QString,int,QString",sTrCode,sRQName,0,"총매입금액")            total_buy_money_result = int(total_buy_money)            print("총매입금액 %s" % total_buy_money_result)            total_profit_loss_rate = self.dynamicCall("GetCommData(QString,QString,int,QString", sTrCode, sRQName, 0, "총수익률(%)")            total_profit_loss_rate_result = float(total_profit_loss_rate)            print("총수익률 %s" % total_profit_loss_rate_result)            rows = self.dynamicCall("GetRepeatCnt(QString,QString)",sTrCode,sRQName)            cnt = 0            for i in range(rows):                code = self.dynamicCall("GetCommData(QString,QString, int, QString)",sTrCode,sRQName,i,"종목번호")                code_nm = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "종목명")                stock_quantity = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "보유수량")                buy_price = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "매입가")                learn_rate = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "수익률(%)")                corrent_price = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "현재가")                total_chegual_price = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "매입금액")                possible_quantity = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "매매가능수량")                code = code.strip()                if code in self.account_stock_dict:                    pass                else:                    self.account_stock_dict[code] = {}                code_nm = code_nm.replace(" ","")                stock_quantity = int(stock_quantity.replace(" ",""))                buy_price = int(buy_price.replace(" ",""))                learn_rate = float(learn_rate.replace(" ",""))                corrent_price = int(corrent_price.replace(" ",""))                total_chegual_price = int(total_chegual_price.replace(" ",""))                possible_quantity = int(possible_quantity.replace(" ",""))                self.account_stock_dict[code]['종목명'] = code_nm                self.account_stock_dict[code]['보유수량'] = stock_quantity                self.account_stock_dict[code]['매입가'] = buy_price                self.account_stock_dict[code]['수익률(%)'] = learn_rate                self.account_stock_dict[code]['현재가'] = corrent_price                self.account_stock_dict[code]['매입금액'] = total_chegual_price                self.account_stock_dict[code]['매매가능수량'] = possible_quantity                cnt+=1;            print("계좌에 가지고 있는 종목 수", cnt)            # print("계좌에 가지고 있는 종목", self.account_stock_dict)            if sPrevNext == "2":                print("종목 두번째 페이지 시작")                self.detail_account_mystock(sPrevNext="2")            else:                print("계좌종목 이벤트루프 끝")                self.detail_account_info_event_loop.exit()        elif sRQName == "실시간미체결요청":            print("실시간여기 왔다")            rows = self.dynamicCall("GetRepeatCnt(QString,QString)", sTrCode, sRQName)            for i in range(rows):                code = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "종목코드")                code_nm = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "종목명")                order_no = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "주문번호")                order_status = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "주문상태")                order_quantity = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "주문수량")                order_price = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "주문가격")                order_gubun = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "주문구분")                not_quantity = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "미체결수량")                ok_quantity = self.dynamicCall("GetCommData(QString,QString, int, QString)", sTrCode, sRQName, i, "체결량")                code = code.strip()                code_nm = code_nm.strip()                order_no = int(order_no.replace(" ", ""))                order_status = order_status.replace(" ", "")                order_quantity = int(order_quantity.replace(" ", ""))                order_price = int(order_price.replace(" ", ""))                order_gubun = order_gubun.replace(" ", "").lstrip('+').lstrip('-')                not_quantity = int(not_quantity.replace(" ", ""))                ok_quantity = int(ok_quantity.replace(" ", ""))                if order_no in self.not_account_stock_dict:                    pass                else:                    self.not_account_stock_dict[order_no] = {}                nasd = self.not_account_stock_dict[order_no]                nasd["종목코드"] = code                nasd["종목명"] = code_nm                nasd["주문번호"] = order_no                nasd["주문상태"] = order_status                nasd["주문수량"] = order_quantity                nasd["주문가격"] = order_price                nasd["주문구분"] = order_gubun                nasd["미체결수량"] = not_quantity                nasd["체결량"] = ok_quantity            print("미체결 종목: %s"% self.not_account_stock_dict)            print("미체결 종목 루프 끝")            self.detail_account_info_event_loop.exit()        elif sRQName == "주식일봉차트조회":            code = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, 0, '종목코드')            code = code.strip()            print("%s 일봉데이터 요청" % code)            # data = self.dynamicCall("GetCommDataEx(QString, QString)", sTrCode, sRQName)            # [[‘’, ‘현재가’, ‘거래량’, ‘거래대금’, ‘날짜’, ‘시가’, ‘고가’, ‘저가’. ‘’], [‘’, ‘현재가’, ’거래량’, ‘거래대금’, ‘날짜’, ‘시가’, ‘고가’, ‘저가’, ‘’]. […]]            cnt = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)            print("남은 일자 수 %s" % cnt)            #한번 조회시 600일치까지 일봉데이터를 받을 수 있다.            for i in range(cnt):                data = []                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)",sTrCode, sRQName, i,"현재가")  # 출력 : 000070                value = self.dynamicCall("GetCommData(QString, QString, int, QString)",sTrCode, sRQName, i,"거래량")  # 출력 : 000070                trading_value = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,"거래대금")  # 출력 : 000070                date = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,"일자")  # 출력 : 000070                start_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,"시가")                high_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,"고가")  # 출력 : 000070                low_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,"저가")  # 출력 : 000070                data.append("")                data.append(current_price.replace(" ", ""))                data.append(value.replace(" ", ""))                data.append(trading_value.replace(" ", ""))                data.append(date.replace(" ", ""))                data.append(start_price.replace(" ", ""))                data.append(high_price.replace(" ", ""))                data.append(low_price.replace(" ", ""))                data.append("")                self.calcul_data.append(data.copy())            # if sPrevNext == "2":            #     self.day_kiwoom_db(code=code, sPrevNext=sPrevNext)            # else:            print("총 일수 %s" % len(self.calcul_data))            pass_success = False            # 120일 이평선을 그릴만큼의 데이터가 있는지 체크            if self.calcul_data == None or len(self.calcul_data) < 120:                pass_success = False            else:                # 120일 이평선의 최근 가격 구함                total_price = 0                for value in self.calcul_data[:120]:                    total_price += int(value[1])                moving_average_price = total_price / 120                # 오늘자 주가가 120일 이평선에 걸쳐있는지 확인                bottom_stock_price = False                check_price = None                if int(self.calcul_data[0][7]) <= moving_average_price and moving_average_price <= int(self.calcul_data[0][6]):                    print("오늘 주가 120이평선 아래에 걸쳐있는 것 확인")                    bottom_stock_price = True                    check_price = int(self.calcul_data[0][6])                # 과거 일봉 데이터를 조회하면서 120일 이평선보다 주가가 계속 밑에 존재하는지 확인                prev_price = None                if bottom_stock_price == True:                    moving_average_price_prev = 0                    price_top_moving = False                    idx = 1                    while True:                        if len(self.calcul_data[idx:]) < 120:  # 120일치가 있는지 계속 확인                            print("120일치가 없음")                            break                        ### 이동 평균선 가격은 날마다 달라지니 과거 데이터 조회할 때마다 구함                        total_price = 0                        for value in self.calcul_data[idx:120 + idx]:                            total_price += int(value[1])                        moving_average_price_prev = total_price / 120                        if moving_average_price_prev <= int(self.calcul_data[idx][6]) and idx <= 20:                            print("20일 동안 주가가 120일 이평선과 같거나 위에 있으면 조건 통과 못함")                            price_top_moving = False                            break                        elif int(self.calcul_data[idx][7]) > moving_average_price_prev and idx > 20:  # 120일 이평선 위에 있는 구간 존재                            print("120일치 이평선 위에 있는 구간 확인됨")                            price_top_moving = True                            prev_price = int(self.calcul_data[idx][7])                            break                        idx += 1                    # 해당부분 이평선이 가장 최근의 이평선 가격보다 낮은지 확인                    if price_top_moving == True:                        if moving_average_price > moving_average_price_prev and check_price > prev_price:                            print("포착된 이평선의 가격이 오늘자 이평선 가격보다 낮은 것 확인")                            print("포착된 부분의 저가가 오늘자 주가의 고가보다 낮은지 확인")                            pass_success = True            if pass_success == True:                print("조건부 통과됨")                code_nm = self.dynamicCall("GetMasterCodeName(QString)", code)                f = open("files/condition_stock.txt", "a", encoding="utf8")                f.write("%s\t%s\t%s\n" % (code, code_nm, str(self.calcul_data[0][1])))                f.close()            elif pass_success == False:                print("조건부 통과 못함")            self.calcul_data.clear()            print("calculator 루프 끝")            self.calculator_event_loop.exit()            # if sPrevNext == "2":            #     self.day_kiwoom_db(code=code,sPrevNext=sPrevNext)            # else:            #     print("calculator 루프 끝")            #     self.calculator_event_loop.exit()    def stop_screen_cancel(self, sScrNo=None):        self.dynamicCall("DisconnectRealData(QString)", sScrNo)  # 스크린번호 연결끊기    def get_code_list_by_market(self,market_code):        '''        종목 코드들 반환        :param market_code:        :return:        '''        code_list = self.dynamicCall("GetCodeListByMarket(QString)",market_code)        code_list = code_list.split(";")[:-1]        return code_list    def calculator_fnc(self):        '''        종목 분석 실행용 함수        :return:        '''        code_list = self.get_code_list_by_market("10")        print("코스닥 갯수", len(code_list))        for idx,code in enumerate(code_list):            self.dynamicCall("DisconnectRealData(QString)",self.screen_calculation_stock)            print("%s / %s : KOSDAQ Strock Code : %s is  updating..." % (idx+1, len(code_list),code))            self.day_kiwoom_db(code = code)    def day_kiwoom_db(self, code=None, date=None, sPrevNext = "0"):        QTest.qWait(3600)        self.dynamicCall("SetInputValue(QString,QString)", "종목코드",code)        self.dynamicCall("SetInputValue(QString,QString)", "수정주가구분", "1")        if date != None:            self.dynamicCall("SetInputValue(QString,QString)", "기준일자", date)        self.dynamicCall("CommRqData(QString,QString,int,QString)", "주식일봉차트조회", "opt10081", sPrevNext,self.screen_calculation_stock)        if sPrevNext == "0":            print("calculator 루프 시작")            self.calculator_event_loop.exec_()    #매수법칙    def read_code(self):        if os.path.exists("files/condition_stock.txt"):            f = open("files/condition_stock.txt","r",encoding="utf8")            lines = f.readlines()            for line in lines:                if line != "":                    ls = line.split("\t")                    stock_code = ls[0]                    stock_name = ls[1]                    stock_price = int(ls[2].split("\n")[0])                    stock_price = abs(stock_price)                    self.portfolio_stock_dict[stock_code] = {}                    psd = self.portfolio_stock_dict[stock_code]                    psd["종목명"] = stock_name                    psd["현재가"] = stock_price            f.close()    def screen_number_setting(self):        screen_overwrite = []        # 계좌평가잔고내역에 있는 종목들        for code in self.account_stock_dict.keys():            if code not in screen_overwrite:                screen_overwrite.append(code)        #미체결에 있는 종목들        for order_number in self.not_account_stock_dict.keys():            code = self.not_account_stock_dict[order_number]['종목코드']            if code not in screen_overwrite:                screen_overwrite.append(code)        #포트폴리오에 담겨있는 종목들        for code in self.portfolio_stock_dict.keys():             if code not in screen_overwrite:                 screen_overwrite.append(code)        #스크린번호 할당        cnt = 0        for code in screen_overwrite:            temp_screen = int(self.screen_real_stock)            meme_screen = int(self.screen_meme_stock)            if (cnt % 50) == 0:                temp_screen +=1                self.screen_real_stock = str(temp_screen)            if (cnt % 50) == 0:                meme_screen += 1                self.screen_meme_stock = str(meme_screen)            if code in self.portfolio_stock_dict.keys():                self.portfolio_stock_dict[code].update({"스크린번호": str(self.screen_real_stock)})                self.portfolio_stock_dict[code].update({"주문용스크린번호": str(self.screen_meme_stock)})            elif code not in self.portfolio_stock_dict.keys():                self.portfolio_stock_dict.update(                    {code: {"스크린번호": str(self.screen_real_stock), "주문용스크린번호": str(self.screen_meme_stock)}})            cnt += 1        print(self.portfolio_stock_dict)    def realdata_slot(self,sCode,sRealType,sRealData):        # print("여기 안옴?",sRealType)        if sRealType == "장시작시간":            fid = self.realType.REALTYPE["장시작시간"]["장운영구분"]            value = self.dynamicCall("GetCommRealData(QString,int)",sCode,fid)            if value == '0':                print("장 시작 전")            elif value == "3":                print("장 시작")            elif value == "2":                print("장 종료, 동시호가로 넘어감")            elif value == "4":                print("3시30분 장 종료")                for code in self.portfolio_stock_dict.keys():                    self.dynamicCall("SetRealRemove(String,String)",self.portfolio_stock_dict[code]['스크린번호'],code)                QTest.qWait(5000)                self.file_delete()                self.calculator_fnc()                sys.exit()        elif sRealType == "주식체결":            print(sCode)            a = self.dynamicCall("GetCommRealData(QString,int)",sCode, self.realType.REALTYPE[sRealType]["체결시간"])            b = self.dynamicCall("GetCommRealData(QString,int)",sCode, self.realType.REALTYPE[sRealType]["현재가"])            b = abs(int(b))            c = self.dynamicCall("GetCommRealData(QString,int)", sCode, self.realType.REALTYPE[sRealType]["전일대비"])            c = abs(int(c))            d = self.dynamicCall("GetCommRealData(QString,int)", sCode, self.realType.REALTYPE[sRealType]["등락율"])            d = float(d)            e = self.dynamicCall("GetCommRealData(QString,int)", sCode, self.realType.REALTYPE[sRealType]["(최우선)매도호가"])            e = abs(int(e))            f = self.dynamicCall("GetCommRealData(QString,int)", sCode, self.realType.REALTYPE[sRealType]["(최우선)매수호가"])            f = abs(int(f))            g = self.dynamicCall("GetCommRealData(QString,int)", sCode, self.realType.REALTYPE[sRealType]["거래량"])            g = abs(int(g))            i = self.dynamicCall("GetCommRealData(QString,int)", sCode, self.realType.REALTYPE[sRealType]["고가"])            i = abs(int(i))            j = self.dynamicCall("GetCommRealData(QString,int)", sCode, self.realType.REALTYPE[sRealType]["시가"])            j = abs(int(j))            k = self.dynamicCall("GetCommRealData(QString,int)", sCode, self.realType.REALTYPE[sRealType]["저가"])            k = abs(int(k))            if sCode not in self.portfolio_stock_dict:                self.portfolio_stock_dict[sCode] = {}            psd = self.portfolio_stock_dict[sCode]            psd["체결시간"] = a            psd["현재가"] = b            psd["전일대비"] = c            psd["등락율"] = d            psd["(최우선)매도호가"] = e            psd["(최우선)매수호가"] = f            psd["거래량"] = g            psd["고가"] = i            psd["시가"] = j            psd["저가"] = k            # print(self.portfolio_stock_dict[sCode])            #계좌잔고평가내역에 있고 오늘 산 잔고에는 없을 경우            if sCode in self.account_stock_dict.keys() and sCode not in self.jango_dict.keys():                asd = self.account_stock_dict[sCode]                meme_rate = (b - asd['매입가'])/ asd['매입가'] * 100                if asd['매매가능수량'] > 0 and (meme_rate > 5 or meme_rate < -5 ):                    order_success = self.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",                                     "신규매도", self.portfolio_stock_dict[sCode]['주문용스크린번호'], self.account_num, 2,                                     sCode, asd['매매가능수량'],0, self.realType.SENDTYPE['거래구분']['시장가'],"")                    if order_success == 0:                        print("매도주문 전달 성공")                        del self.account_stock_dict[sCode]                    else:                        print("매도주문 전달 실패")            # 오늘 산 잔고에 있을 경우            elif sCode in self.jango_dict.keys():                jd = self.jango_dict[sCode]                meme_rate = ( b - jd['매입단가']) / jd['매입단가'] * 100                if jd['주문가능수량'] > 0 and ( meme_rate > 5 or meme_rate < -5):                    order_success = self.dynamicCall(                        "SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",                        ["신규매도", self.portfolio_stock_dict[sCode]["주문용스크린번호"], self.account_num, 2, sCode, jd['주문가능수량'],                         0,self.realType.SENDTYPE['거래구분']['시장가'],""]                    )                    if order_success == 0:                        print("매도주문 전달 성공")                    else:                        print("매도주문 전달 실패")            # 등락율이 2.0% 이상이고 오늘 산 잔고에 없을 경우우            elif d > 2.0 and sCode not in self.jango_dict:                result = (self.use_money * 0.1) / e                quantity = int(result)                order_success = self.dynamicCall(                    "SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",                    ["신규매수", self.portfolio_stock_dict[sCode]["주문용스크린번호"],self.account_num,1,sCode,quantity,e,self.realType.SENDTYPE['거래구분']['지정가'],""]                )                if order_success == 0:                    print("매수주문 전달 성공")                else:                    print("매수주문 전달 실패패")            not_meme_list =list(self.not_account_stock_dict)            for order_num in not_meme_list:                code = self.not_account_stock_dict[order_num]["종목코드"]                meme_price = self.not_account_stock_dict[order_num]['주문가격']                not_quantity = self.not_account_stock_dict[order_num]['미체결수량']                order_gubun = self.not_account_stock_dict[order_num]['주문구분']                if order_gubun == "매수" and not_quantity > 0 and e > meme_price:                    order_success = self.dynamicCall(                        "SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",                        ["매수취소", self.portfolio_stock_dict[sCode]["주문용스크린번호"], self.account_num, 3,code,0,0,                         self.realType.SENDTYPE['거래구분']['지정가'], order_num]                    )                    if order_success == 0:                        print("매수취소 전달 성공")                    else:                        print("매수취소 전달 실패")                elif not_quantity == 0:                    del self.not_account_stock_dict[order_num]    def chejan_slot(self,sGubun,nItemCnt,sFIdList):        print("여기 안들어오나본데",sGubun)        if int(sGubun) == 0:            account_num = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['계좌번호'])            sCode = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['종목코드'])[1:]            stock_name = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['종목명'])            stock_name = stock_name.strip()            origin_order_number = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['원주문번호'])  # 출력 : defaluse : "000000"            order_number = self.dynamicCall("GetChejanData(int)",self.realType.REALTYPE['주문체결']['주문번호'])  # 출럭: 0115061 마지막 주문번호            order_status = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문상태'])  # 출력: 접수, 확인, 체결            order_quan = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문수량'])  # 출력 : 3            order_quan = int(order_quan)            order_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문가격'])  # 출력: 21000            order_price = int(order_price)            not_chegual_quan = self.dynamicCall("GetChejanData(int)",self.realType.REALTYPE['주문체결']['미체결수량'])  # 출력: 15, default: 0            not_chegual_quan = int(not_chegual_quan)            order_gubun = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문구분'])  # 출력: -매도, +매수            order_gubun = order_gubun.strip().lstrip('+').lstrip('-')            chegual_time_str = self.dynamicCall("GetChejanData(int)",self.realType.REALTYPE['주문체결']['주문/체결시간'])  # 출력: '151028'            chegual_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['체결가'])  # 출력: 2110  default : ''            if chegual_price == '':                chegual_price = 0            else:                chegual_price = int(chegual_price)            chegual_quantity = self.dynamicCall("GetChejanData(int)",self.realType.REALTYPE['주문체결']['체결량'])  # 출력: 5  default : ''            if chegual_quantity == '':                chegual_quantity = 0            else:                chegual_quantity = int(chegual_quantity)            current_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['현재가'])  # 출력: -6000            current_price = abs(int(current_price))            first_sell_price = self.dynamicCall("GetChejanData(int)",self.realType.REALTYPE['주문체결']['(최우선)매도호가'])  # 출력: -6010            first_sell_price = abs(int(first_sell_price))            first_buy_price = self.dynamicCall("GetChejanData(int)",self.realType.REALTYPE['주문체결']['(최우선)매수호가'])  # 출력: -6000            first_buy_price = abs(int(first_buy_price))            ######## 새로 들어온 주문이면 주문번호 할당            if order_number not in self.not_account_stock_dict.keys():                self.not_account_stock_dict.update({order_number: {}})            self.not_account_stock_dict[order_number].update({"종목코드": sCode})            self.not_account_stock_dict[order_number].update({"주문번호": order_number})            self.not_account_stock_dict[order_number].update({"종목명": stock_name})            self.not_account_stock_dict[order_number].update({"주문상태": order_status})            self.not_account_stock_dict[order_number].update({"주문수량": order_quan})            self.not_account_stock_dict[order_number].update({"주문가격": order_price})            self.not_account_stock_dict[order_number].update({"미체결수량": not_chegual_quan})            self.not_account_stock_dict[order_number].update({"원주문번호": origin_order_number})            self.not_account_stock_dict[order_number].update({"주문구분": order_gubun})            self.not_account_stock_dict[order_number].update({"주문/체결시간": chegual_time_str})            self.not_account_stock_dict[order_number].update({"체결가": chegual_price})            self.not_account_stock_dict[order_number].update({"체결량": chegual_quantity})            self.not_account_stock_dict[order_number].update({"현재가": current_price})            self.not_account_stock_dict[order_number].update({"(최우선)매도호가": first_sell_price})            self.not_account_stock_dict[order_number].update({"(최우선)매수호가": first_buy_price})            print(self.not_account_stock_dict)        elif int(sGubun) == 1:            # print("잔고구분")            account_num = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['계좌번호'])            sCode = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['종목코드'])[1:]            stock_name = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['종목명'])            stock_name = stock_name.strip()            current_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['현재가'])            current_price = abs(int(current_price))            stock_quan = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['보유수량'])            stock_quan = int(stock_quan)            like_quan = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['주문가능수량'])            like_quan = int(like_quan)            buy_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['매입단가'])            buy_price = abs(int(buy_price))            total_buy_price = self.dynamicCall("GetChejanData(int)",                                               self.realType.REALTYPE['잔고']['총매입가'])  # 계좌에 있는 종목의 총매입가            total_buy_price = int(total_buy_price)            meme_gubun = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['매도매수구분'])            meme_gubun = self.realType.REALTYPE['매도수구분'][meme_gubun]            first_sell_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['(최우선)매도호가'])            first_sell_price = abs(int(first_sell_price))            first_buy_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['(최우선)매수호가'])            first_buy_price = abs(int(first_buy_price))            if sCode not in self.jango_dict.keys():                self.jango_dict.update({sCode: {}})            self.jango_dict[sCode].update({"현재가": current_price})            self.jango_dict[sCode].update({"종목코드": sCode})            self.jango_dict[sCode].update({"종목명": stock_name})            self.jango_dict[sCode].update({"보유수량": stock_quan})            self.jango_dict[sCode].update({"주문가능수량": like_quan})            self.jango_dict[sCode].update({"매입단가": buy_price})            self.jango_dict[sCode].update({"총매입가": total_buy_price})            self.jango_dict[sCode].update({"매도매수구분": meme_gubun})            self.jango_dict[sCode].update({"(최우선)매도호가": first_sell_price})            self.jango_dict[sCode].update({"(최우선)매수호가": first_buy_price})            if stock_quan == 0:                del self.jango_dict[sCode]                self.dynamicCall("SetRealRemove(QString,QString)", self.portfolio_stock_dict[sCode]['스크린번호'],sCode)    #송수신 메세지 get    def msg_slot(self, sScrNo, sRQName, sTrCode, msg):        print("스크린: %s, 요청이름: %s, tr코드: %s --- %s" %(sScrNo, sRQName, sTrCode, msg))    #파일 삭제    def file_delete(self):        if os.path.isfile("files/condition_stock.txt"):            os.remove("files/condition_stock.txt")