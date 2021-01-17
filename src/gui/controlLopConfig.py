#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from simpleFOCConnector import SimpleFOCDevice

class ControlLoopGroupBox(QtWidgets.QGroupBox):
    def __init__(self, parent=None,simpleFocConn=None):
        """Constructor for ToolsWidget"""
        super().__init__(parent)

        self.device = simpleFocConn

        self.setObjectName("controlLoopGroupBox")
        self.setTitle("Control Loop Mode")

        self.controlLoopHorizontalLayout = QtWidgets.QHBoxLayout(self)
        self.controlLoopHorizontalLayout.setObjectName("controlLoopHorizontalLayout")

        self.angleRadioButton = QtWidgets.QRadioButton(self)
        self.angleRadioButton.setObjectName("angleRadioButton")
        self.angleRadioButton.setText("Angle")
        self.angleRadioButton.toggled.connect(self.sendControlLopModeAngle)
        self.controlLoopHorizontalLayout.addWidget(self.angleRadioButton)

        self.velocityRadioButton = QtWidgets.QRadioButton(self)
        self.velocityRadioButton.setObjectName("velocityRadioButton")
        self.velocityRadioButton.setText("Velocity")
        self.velocityRadioButton.toggled.connect(self.sendControlLopModeVelocity)
        self.controlLoopHorizontalLayout.addWidget(self.velocityRadioButton)

        self.voltageRadioButton = QtWidgets.QRadioButton(self)
        self.voltageRadioButton.setObjectName("voltageRadioButton")
        self.voltageRadioButton.setText("Voltage")
        self.voltageRadioButton.toggled.connect(self.sendControlLopModeVoltage)
        self.controlLoopHorizontalLayout.addWidget(self.voltageRadioButton)

        self.setControlLopMode(self.device.controlType)

        self.disableUI()
        self.device.addConnectionStateListener(self)

    def deviceConnected(self, deviceConnected):
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
        self.device.sendControlType(SimpleFOCDevice.VELOCITY_CONTROL)

    def sendControlLopModeAngle(self):
        self.device.sendControlType(SimpleFOCDevice.ANGLE_CONTROL)

    def sendControlLopModeVoltage(self):
        self.device.sendControlType(SimpleFOCDevice.VOLTAGE_CONTROL)