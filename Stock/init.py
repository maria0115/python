import sys
sys.path.append('D:\PYTHON\Stock')

from analysis.stockanalysis import *
class Main():
    def __init__(self):
        print("실행할 메인 클래스")
        Analysis()


if __name__ == "__main__":
    Main()