# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:28:58 2023

@author: jellyho
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time, sys
from RCServer import RCServer

# do not modify
app = QApplication(sys.argv)
rc = RCServer()

####
class MainWorker(QObject):    
    @pyqtSlot()
    def main(self):
        # main training Code Here :)
        while True:
            while rc.available():
                rc.worker.Act('A', 'W')
                time.sleep(1)
                rc.worekr.Act('A', 'S')
                time.sleep(1)
            print('Robots are not available')
            time.sleep(1)
        return
 ####   
    
# do not modifiy
main = MainWorker()
rc.setMain(main)
rc.show()
sys.exit(app.exec_())
