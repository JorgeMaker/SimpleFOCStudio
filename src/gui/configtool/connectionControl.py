#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from src.simpleFOCConnector import SimpleFOCDevice
from src.gui.sharedcomnponets.sharedcomponets import GUIToolKit
from src.gui.configtool.configureConnectionDialog import ConfigureSerailConnectionDialog

class ConnectionControlGroupBox(QtWidgets.QGroupBox):

    def __init__(self, parent=None,simpleFocConn=None):
        super().__init__(parent)

        self.device = simpleFocConn

        self.setObjectName('connectionControl')
        self.setTitle('Connection control')

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName('generalControlHL')

        self.connectionModeComboBox = QtWidgets.QComboBox()
        self.connectionModeComboBox.setObjectName('connectDeviceButton')
        self.connectionModeComboBox.addItems([SimpleFOCDevice.PULL_CONFIG_ON_CONNECT,SimpleFOCDevice.PUSH_CONFG_ON_CONNECT])

        self.horizontalLayout.addWidget(self.connectionModeComboBox)

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

    def connectDisconnectDeviceAction(self):

        if self.device.isConnected:
            self.device.disConnect()
            self.connectDisconnectButton.setIcon(
                GUIToolKit.getIconByName('connect'))
            self.connectDisconnectButton.setText('Connect')

        else:
            connectionMode  = self.connectionModeComboBox.currentText()
            hasBeenConnected  = self.device.connect(connectionMode)
            if hasBeenConnected:
                self.connectDisconnectButton.setIcon(
                    GUIToolKit.getIconByName('disconnect'))
                self.connectDisconnectButton.setText('Disconnect')


    def configureDeviceAction(self):
        dialog = ConfigureSerailConnectionDialog(self.device)
        result = dialog.exec_()
        if result:
            deviceConfig = dialog.getConfigValues()
            self.device.configureDevice(deviceConfig)
