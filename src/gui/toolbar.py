# !/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from gui.sharedcomponets import GUIToolKit

class SimpleFOCConfigToolBar(QtWidgets.QToolBar):
    """ This class is used to create a tool bar to launch a tool to manage each
        available device to be configured
    """
    def __init__(self,main_window, devicesTabedWidget,  parent=None):
        super().__init__(parent)

        self.addDeviceAction = QtWidgets.QAction(main_window)
        self.addDeviceAction.setIcon(GUIToolKit.getIconByName("add"))
        self.addDeviceAction.setObjectName("addDeviceAction")
        self.addDeviceAction.triggered.connect(devicesTabedWidget.addDevice)
        self.addAction(self.addDeviceAction)

        self.openDeviceAction = QtWidgets.QAction(main_window)
        self.openDeviceAction.setIcon(GUIToolKit.getIconByName("open"))
        self.openDeviceAction.setObjectName("openDeviceAction")
        self.openDeviceAction.triggered.connect(devicesTabedWidget.openDevice)
        self.addAction(self.openDeviceAction)

        self.saveDeviceAction = QtWidgets.QAction(main_window)
        self.saveDeviceAction.setIcon(GUIToolKit.getIconByName("save"))
        self.saveDeviceAction.setObjectName("saveDeviceAction")
        self.saveDeviceAction.triggered.connect(devicesTabedWidget.saveDevice)
        self.addAction(self.saveDeviceAction)

        self.addSeparator()
