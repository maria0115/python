import sys

sys.path.append('D:\\PYTHON\\autostock')
print(sys.path)

from ui.ui import *
class Main():
    def __init__(self):
        print("실행할 메인 클래스")
        UI_class()

if __name__ == "__main__":
    Main()