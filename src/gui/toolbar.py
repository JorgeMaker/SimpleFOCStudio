# !/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from src.gui.sharedcomnponets.sharedcomponets import GUIToolKit


class SimpleFOCConfigToolBar(QtWidgets.QToolBar):

    def __init__(self,main_window, devicesTabedWidget,  parent=None):
        super().__init__(parent)
        
        self.addDeviceAction = QtWidgets.QToolButton(main_window)
        self.addDeviceAction.setIcon(GUIToolKit.getIconByName('add_motor'))
        self.addDeviceAction.setObjectName('addDeviceAction')
        self.addDeviceAction.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        self.addDeviceMenu = QtWidgets.QMenu(self.addDeviceAction)
        self.addDeviceTreeView  = QtWidgets.QAction("Tree View",self.addDeviceMenu)
        self.addDeviceTreeView.setIcon(GUIToolKit.getIconByName('tree'))
        self.addDeviceTreeView.triggered.connect(devicesTabedWidget.addDeviceTree)
        self.addDeviceFormView  = QtWidgets.QAction("Form View",self.addDeviceMenu)
        self.addDeviceFormView.setIcon(GUIToolKit.getIconByName('form'))
        self.addDeviceFormView.triggered.connect(devicesTabedWidget.addDeviceForm)
        
        self.addDeviceMenu.addAction(self.addDeviceTreeView)
        self.addDeviceMenu.addAction(self.addDeviceFormView)
        self.addDeviceAction.setMenu(self.addDeviceMenu)
        self.addWidget(self.addDeviceAction)

        self.openDeviceAction = QtWidgets.QAction(main_window)
        self.openDeviceAction.setIcon(GUIToolKit.getIconByName('open'))
        self.openDeviceAction.setObjectName('openDeviceAction')
        self.openDeviceAction.triggered.connect(devicesTabedWidget.openDevice)

        self.addAction(self.openDeviceAction)

        self.saveDeviceAction = QtWidgets.QAction(main_window)
        self.saveDeviceAction.setIcon(GUIToolKit.getIconByName('save'))
        self.saveDeviceAction.setObjectName('saveDeviceAction')
        self.saveDeviceAction.triggered.connect(devicesTabedWidget.saveDevice)

        self.addAction(self.saveDeviceAction)

        self.generateCodeAction = QtWidgets.QAction(main_window)
        self.generateCodeAction.setIcon(GUIToolKit.getIconByName('gen'))
        self.generateCodeAction.setObjectName('genertecode')
        self.generateCodeAction.triggered.connect(devicesTabedWidget.generateCode)

        self.addAction(self.generateCodeAction)
        self.addSeparator()

        self.openConsoleToolAction = QtWidgets.QAction(main_window)
        self.openConsoleToolAction.setIcon(GUIToolKit.getIconByName('consoletool'))
        self.openConsoleToolAction.setToolTip('Open Serial Cosole tool')
        self.openConsoleToolAction.setObjectName('openconsoletool')
        self.openConsoleToolAction.triggered.connect(devicesTabedWidget.openConsoleTool)

        self.addAction(self.openConsoleToolAction)

        self.addSeparator()
