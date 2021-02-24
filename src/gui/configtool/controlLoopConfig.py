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

        self.angleRadioButton = QtWidgets.QRadioButton(self)
        self.angleRadioButton.setObjectName('angleRadioButton')
        self.angleRadioButton.setText('Angle')
        self.angleRadioButton.clicked.connect(self.sendControlLopModeAngle)
        self.controlLoopHorizontalLayout.addWidget(self.angleRadioButton)

        self.velocityRadioButton = QtWidgets.QRadioButton(self)
        self.velocityRadioButton.setObjectName('velocityRadioButton')
        self.velocityRadioButton.setText('Velocity')
        self.velocityRadioButton.clicked.connect(self.sendControlLopModeVelocity)
        self.controlLoopHorizontalLayout.addWidget(self.velocityRadioButton)

        self.voltageRadioButton = QtWidgets.QRadioButton(self)
        self.voltageRadioButton.setObjectName('voltageRadioButton')
        self.voltageRadioButton.setText('Voltage')
        self.voltageRadioButton.clicked.connect(self.sendControlLopModeVoltage)
        self.controlLoopHorizontalLayout.addWidget(self.voltageRadioButton)

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
        if value == SimpleFOCDevice.ANGLE_CONTROL:
            self.angleRadioButton.toggle()
        elif value == SimpleFOCDevice.VOLTAGE_CONTROL:
            self.voltageRadioButton.toggle()
        elif value == SimpleFOCDevice.VELOCITY_CONTROL:
            self.velocityRadioButton.toggle()

    def sendControlLopModeVelocity(self):
        if self.device.isConnected:
            self.device.sendControlType(SimpleFOCDevice.VELOCITY_CONTROL)
    def sendControlLopModeAngle(self):
        if self.device.isConnected:
            self.device.sendControlType(SimpleFOCDevice.ANGLE_CONTROL)

    def sendControlLopModeVoltage(self):
        if self.device.isConnected:
            self.device.sendControlType(SimpleFOCDevice.VOLTAGE_CONTROL)

    def commandResponseReceived(self, cmdRespose):
        if 'Control: ' in cmdRespose:
            self.setControlLopMode((SimpleFOCDevice.getControlModeCode(cmdRespose.replace('Control: ', ''))))