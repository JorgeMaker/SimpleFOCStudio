#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import (QtGui, QtWidgets, QtCore)

from src.gui.sharedcomnponets.sharedcomponets import GUIToolKit
from src.simpleFOCConnector import SimpleFOCDevice


class GeneralControls(QtWidgets.QGroupBox):

    def __init__(self, parent=None):

        super().__init__(parent)

        # self.setMaximumWidth(300)

        onlyFloat = QtGui.QRegExpValidator(
            QtCore.QRegExp("[+-]?([0-9]*[.])?[0-9]+"))

        self.device = SimpleFOCDevice.getInstance()

        self.setTitle('General Controls')

        self.setObjectName('generalControls')

        self.gcGridLayout = QtWidgets.QGridLayout(self)
        self.gcGridLayout.setObjectName('gcGridLayout')


        self.enableDeviceButton = QtWidgets.QPushButton(self)
        self.enableDeviceButton.setObjectName('enButton')
        self.enableDeviceButton.setText('Enable Device')
        self.enableDeviceButton.setIcon(GUIToolKit.getIconByName('greendot'))
        self.enableDeviceButton.clicked.connect(self.toggleEnable)
        self.gcGridLayout.addWidget(self.enableDeviceButton, 1, 0, 1, 1)

        self.sensorZeroButton = QtWidgets.QPushButton(self)
        self.sensorZeroButton.setObjectName('homeButton')
        self.sensorZeroButton.setText('Sensor Zero')
        self.sensorZeroButton.setIcon(GUIToolKit.getIconByName('home'))
        self.sensorZeroButton.clicked.connect(self.setSensorZero)
        self.gcGridLayout.addWidget(self.sensorZeroButton, 1, 1, 1, 1)

        self.setZeroTarget = QtWidgets.QPushButton(self)
        self.setZeroTarget.setObjectName('zeroButton')
        self.setZeroTarget.setText('Zero Target')
        self.setZeroTarget.setIcon(GUIToolKit.getIconByName('stop'))
        self.setZeroTarget.clicked.connect(self.setTargetZero)
        self.gcGridLayout.addWidget(self.setZeroTarget, 1, 2, 1, 1)
        self.reloadValues()

        self.device.addConnectionStateListener(self)
        self.device.commProvider.commandDataReceived.connect(self.commandResponseReceived)

        self.connectionStateChanged(self.device.isConnected)

    def connectionStateChanged(self, deviceConnected):
        if deviceConnected is True:
            self.enabeUI()
        else:
            self.disableUI()

    def enabeUI(self):
        self.setEnabled(True)

    def disableUI(self):
        self.setEnabled(False)

    def setSensorZero(self):
        val = self.device.angleNow + self.device.sensorZeroOffset
        self.device.sendSensorZeroOffset(val)

    def setTargetZero(self):
        self.device.sendTargetValue(0)
    
    def toggleEnable(self):
        val = int( not self.device.deviceStatus)
        self.device.sendDeviceStatus(val)

    def commandResponseReceived(self, comandResponse):
        self.reloadValues()
        
    def reloadValues(self):
        if self.device.deviceStatus:
            self.enableDeviceButton.setText('Disable Device')
            self.enableDeviceButton.setIcon(GUIToolKit.getIconByName('reddot'))
        else:
            self.enableDeviceButton.setText('Enable Device')
            self.enableDeviceButton.setIcon(GUIToolKit.getIconByName('greendot'))