# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:28:58 2023

@author: jellyho
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time, sys
from RCServer import RCServer
import cv2

# do not modify
app = QApplication(sys.argv)
rc = RCServer(port=1234)

####
class MainWorker(QObject):    
    @pyqtSlot()
    def main(self):
        # main training Code Here :)
        self.capture = cv2.VideoCapture(1)
        while True:
            ret, frame = self.capture.read()
            if ret:
                # OpenCV 프레임을 PyQt 이미지로 변환
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                status = 'dreams come true'
                rc.updateStatus(rgb_frame, status)
        return
 ####   
    
# do not modifiy
main = MainWorker()
rc.setMain(main)
rc.show()
sys.exit(app.exec_())
