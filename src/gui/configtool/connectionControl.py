#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from src.gui.configtool.configureConnectionDialog import \
    ConfigureSerailConnectionDialog
from src.gui.sharedcomnponets.sharedcomponets import GUIToolKit
from src.simpleFOCConnector import SimpleFOCDevice


class ConnectionControlGroupBox(QtWidgets.QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.device = SimpleFOCDevice.getInstance()

        self.setObjectName('connectionControl')
        self.setTitle('Connection control')

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName('generalControlHL')

        self.devCommandIDLabel = QtWidgets.QLabel("Command:")
        self.horizontalLayout.addWidget(self.devCommandIDLabel)

        self.devCommandIDLetter = QtWidgets.QLineEdit()
        self.devCommandIDLetter.setObjectName('devCommandIDLetter')
        self.devCommandIDLetter.editingFinished.connect(self.changeDevicedevCommandID)
        self.horizontalLayout.addWidget(self.devCommandIDLetter)
        self.devCommandIDLetter.setText(self.device.devCommandID)

        self.pullConfig = QtWidgets.QPushButton()
        self.pullConfig.setObjectName('pullConfig')
        self.pullConfig.setIcon(GUIToolKit.getIconByName('pull'))
        self.pullConfig.setText(' Pull Params')
        self.pullConfig.clicked.connect(self.device.pullConfiguration)
        
        self.horizontalLayout.addWidget(self.pullConfig)

        self.connectDisconnectButton = QtWidgets.QPushButton(self)
        self.connectDisconnectButton.setIcon(GUIToolKit.getIconByName('connect'))
        self.connectDisconnectButton.setObjectName('connectDeviceButton')
        self.connectDisconnectButton.setText('Connect')
        self.connectDisconnectButton.clicked.connect(self.connectDisconnectDeviceAction)

        self.horizontalLayout.addWidget(self.connectDisconnectButton)

        self.configureDeviceButton = QtWidgets.QPushButton(self)
        self.configureDeviceButton.setIcon(GUIToolKit.getIconByName('configure'))
        self.configureDeviceButton.setObjectName('configureDeviceButton')
        self.configureDeviceButton.setText('Configure')
        self.configureDeviceButton.clicked.connect(self.configureDeviceAction)
        self.horizontalLayout.addWidget(self.configureDeviceButton)

        self.device.addConnectionStateListener(self)
        self.connectionStateChanged(self.device.isConnected)
    
    def changeDevicedevCommandID(self):
        self.device.devCommandID = self.devCommandIDLetter.text()

    def connectDisconnectDeviceAction(self):
        if self.device.isConnected:
            self.device.disConnect()
        else:
            connectionMode  = SimpleFOCDevice.PULL_CONFIG_ON_CONNECT
            self.device.connect(connectionMode)

    def connectionStateChanged(self, isConnected):
        if isConnected:
            self.connectDisconnectButton.setIcon(
                GUIToolKit.getIconByName('disconnect'))
            self.connectDisconnectButton.setText('Disconnect')
        else:
            self.connectDisconnectButton.setIcon(
                GUIToolKit.getIconByName('connect'))
            self.connectDisconnectButton.setText('Connect')

    def configureDeviceAction(self):
        dialog = ConfigureSerailConnectionDialog()
        result = dialog.exec_()
        if result:
            deviceConfig = dialog.getConfigValues()
            self.device.configureConnection(deviceConfig)
