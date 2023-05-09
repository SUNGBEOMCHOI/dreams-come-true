# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:28:58 2023

@author: jellyho
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time


class MainWorker(QObject):    
    @pyqtSlot()
    def main(self):
        # main training Code Here :)
        while True:
            print("Main Thread!")
            time.sleep(1)
        return
    
    
    
    
    
# do not modifiy
from RCServer import start  
main = MainWorker()
start(main)