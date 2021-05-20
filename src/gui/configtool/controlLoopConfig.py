#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from src.simpleFOCConnector import SimpleFOCDevice


class ControlLoopGroupBox(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.device = SimpleFOCDevice.getInstance()

        self.setObjectName('controlLoop')
        self.setTitle('Control Loop Mode')

        self.controlLoopHorizontalLayout = QtWidgets.QHBoxLayout(self)
        self.controlLoopHorizontalLayout.setObjectName('controlLoopHorizontalLayout')

        
        self.selectorControlLoop = QtWidgets.QComboBox(self)
        self.selectorControlLoop.setObjectName('selectorControlLoop')
        self.selectorControlLoop.addItems(['Torque', 'Velocity', 'Angle', 'Velocity openloop', 'Angle openloop'])
        self.selectorControlLoop.currentIndexChanged.connect(self.changeControlLoop)
        self.controlLoopHorizontalLayout.addWidget(self.selectorControlLoop)

        self.setControlLopMode(self.device.controlType)

        self.disableUI()
        self.device.addConnectionStateListener(self)
        self.device.commProvider.commandDataReceived.connect(
            self.commandResponseReceived)

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

    def setControlLopMode(self, value):
        if value == SimpleFOCDevice.TORQUE_CONTROL:
            self.selectorControlLoop.setCurrentIndex(0)
        elif value == SimpleFOCDevice.VELOCITY_CONTROL:
            self.selectorControlLoop.setCurrentIndex(1)
        elif value == SimpleFOCDevice.ANGLE_CONTROL:
            self.selectorControlLoop.setCurrentIndex(2)
        elif value == SimpleFOCDevice.VELOCITY_OPENLOOP_CONTROL:
            self.selectorControlLoop.setCurrentIndex(3)
        elif value == SimpleFOCDevice.ANGLE_OPENLOOP_CONTROL:
            self.selectorControlLoop.setCurrentIndex(4)

    def changeControlLoop(self):
        index = self.selectorControlLoop.currentIndex()
        if index == 0:
            self.device.sendControlType(SimpleFOCDevice.TORQUE_CONTROL)
        elif index == 1:
            self.device.sendControlType(SimpleFOCDevice.VELOCITY_CONTROL)
        elif index == 2:
            self.device.sendControlType(SimpleFOCDevice.ANGLE_CONTROL)
        elif index == 3:
            self.device.sendControlType(SimpleFOCDevice.VELOCITY_OPENLOOP_CONTROL)
        elif index == 4:
            self.device.sendControlType(SimpleFOCDevice.ANGLE_OPENLOOP_CONTROL)

    def commandResponseReceived(self, cmdRespose):
        self.setControlLopMode(self.device.controlType)