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


        self.torqueRadioButton = QtWidgets.QRadioButton(self)
        self.torqueRadioButton.setObjectName('torqueRadioButton')
        self.torqueRadioButton.setText('Torque')
        self.torqueRadioButton.clicked.connect(self.sendControlLopModeTorque)
        self.controlLoopHorizontalLayout.addWidget(self.torqueRadioButton)

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

        self.velocityOpenRadioButton = QtWidgets.QRadioButton(self)
        self.velocityOpenRadioButton.setObjectName('velocityOpenRadioButton')
        self.velocityOpenRadioButton.setText('Velocity open')
        self.velocityOpenRadioButton.clicked.connect(self.sendControlLopModeVelocityOpen)
        self.controlLoopHorizontalLayout.addWidget(self.velocityOpenRadioButton)

        self.angleOpenRadioButton = QtWidgets.QRadioButton(self)
        self.angleOpenRadioButton.setObjectName('angleOpenRadioButton')
        self.angleOpenRadioButton.setText('Angle open')
        self.angleOpenRadioButton.clicked.connect(self.sendControlLopModeAngleOpen)
        self.controlLoopHorizontalLayout.addWidget(self.angleOpenRadioButton)

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
            self.torqueRadioButton.toggle()
        elif value == SimpleFOCDevice.ANGLE_CONTROL:
            self.angleRadioButton.toggle()
        elif value == SimpleFOCDevice.VELOCITY_CONTROL:
            self.velocityRadioButton.toggle()
        elif value == SimpleFOCDevice.VELOCITY_OPENLOOP_CONTROL:
            self.velocityOpenRadioButton.toggle()
        elif value == SimpleFOCDevice.ANGLE_OPENLOOP_CONTROL:
            self.angleOpenRadioButton.toggle()

    def sendControlLopModeVelocity(self):
        if self.device.isConnected:
            self.device.sendControlType(SimpleFOCDevice.VELOCITY_CONTROL)
    def sendControlLopModeAngle(self):
        if self.device.isConnected:
            self.device.sendControlType(SimpleFOCDevice.ANGLE_CONTROL)
    def sendControlLopModeTorque(self):
        if self.device.isConnected:
            self.device.sendControlType(SimpleFOCDevice.TORQUE_CONTROL)
    def sendControlLopModeVelocityOpen(self):
        if self.device.isConnected:
            self.device.sendControlType(SimpleFOCDevice.VELOCITY_OPENLOOP_CONTROL)
    def sendControlLopModeAngleOpen(self):
        if self.device.isConnected:
            self.device.sendControlType(SimpleFOCDevice.ANGLE_OPENLOOP_CONTROL)
            

    def commandResponseReceived(self, cmdRespose):
        self.setControlLopMode(self.device.controlType)