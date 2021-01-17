#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This module contains ans script to start the SimpleFOC ConfigTool, a GIU
    application ta monitor, tune and configure BLDC motor controllers based on
    SimpleFOC library.
"""
from PyQt5 import QtWidgets
from gui.mainWindow import UserInteractionMainWindow
import logging

import sys

if __name__ == "__main__":

    logging.basicConfig(filename='SimpleFOCConfigTool.log', filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    userInteractionMainWindow = UserInteractionMainWindow()
    userInteractionMainWindow.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
