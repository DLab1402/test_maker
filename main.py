import os
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets

from setting import GUI_PATH
from function import data_handle,compose

class main(QtWidgets.QMainWindow):
    cur_subject = ''
    chap_list = []
    def __init__(self):
        super(main,self).__init__() 
        uic.loadUi(GUI_PATH,self)
        self.dataload = data_handle(self)
        self.dataload.begin_load()
        self.dataload.chapter_load()
        self.composer = compose(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    widget.setFixedWidth(1240)
    widget.setFixedHeight(671)
    actor = main()
    widget.addWidget(actor)
    widget.show()
    try:
        sys.exit(app.exec())
    except:
        print("Exiting") 