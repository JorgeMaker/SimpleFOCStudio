#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import (QtCore, QtWidgets)

from src.gui.toolbar import SimpleFOCConfigToolBar
from src.gui.workAreaTabbedWidget import WorkAreaTabbedWidget


class UserInteractionMainWindow(object):

    def setupUi(self, main_window):

        main_window.setObjectName('MainWindow')
        main_window.resize(1300, 900)
        main_window.setWindowTitle('SimpleFOC Configuration Tool ')

        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName('centralwidget')

        # Add layout de to the main window
        self.horizontalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName('verticalLayout')

        # Add tabebd tools widget to the main  window
        self.tabbedToolsWidget = WorkAreaTabbedWidget(self.centralwidget)
        self.horizontalLayout.addWidget(self.tabbedToolsWidget)

        # Add toolbar to the main window
        self.toolBar = SimpleFOCConfigToolBar(main_window,self.tabbedToolsWidget, main_window)
        main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        # Add status bar to the main window
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName('statusbar')
        main_window.setStatusBar(self.statusbar)

        # Add central Widget to the main window
        main_window.setCentralWidget(self.centralwidget)

