#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from src.simpleFOCConnector import SimpleFOCDevice

class TorqueGroupBox(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.device = SimpleFOCDevice.getInstance()

        self.setObjectName('torqueMode')
        self.setTitle('Torque Mode')
        
        self.torqueTypeHorizontalLayout = QtWidgets.QHBoxLayout(self)
        self.torqueTypeHorizontalLayout.setObjectName('torqueHorizontalLayout')


        self.voltageRadioButton = QtWidgets.QRadioButton(self)
        self.voltageRadioButton.setObjectName('voltageRadioButton')
        self.voltageRadioButton.setText('Voltage')
        self.voltageRadioButton.clicked.connect(self.sendTorqueModeVoltage)
        self.torqueTypeHorizontalLayout.addWidget(self.voltageRadioButton)

        self.dcCurrentRadioButton = QtWidgets.QRadioButton(self)
        self.dcCurrentRadioButton.setObjectName('dcCurrentRadioButton')
        self.dcCurrentRadioButton.setText('DC Current')
        self.dcCurrentRadioButton.clicked.connect(self.sendTorqueModeDCCurrent)
        self.torqueTypeHorizontalLayout.addWidget(self.dcCurrentRadioButton)

        self.focCurrentRadioButton = QtWidgets.QRadioButton(self)
        self.focCurrentRadioButton.setObjectName('focCurrentRadioButton')
        self.focCurrentRadioButton.setText('FOC Current')
        self.focCurrentRadioButton.clicked.connect(self.sendTorqueModeFOCCurrent)
        self.torqueTypeHorizontalLayout.addWidget(self.focCurrentRadioButton)

        self.setTorqueMode(self.device.torqueType)

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

    def setTorqueMode(self, value):
        if value == SimpleFOCDevice.VOLTAGE_TORQUE:
            self.voltageRadioButton.toggle()
        elif value == SimpleFOCDevice.DC_CURRENT_TORQUE:
            self.dcCurrentRadioButton.toggle()
        elif value == SimpleFOCDevice.FOC_CURRENT_TORQUE:
            self.focCurrentRadioButton.toggle()

    def sendTorqueModeVoltage(self):
        if self.device.isConnected:
            self.device.sendTorqueType(SimpleFOCDevice.VOLTAGE_TORQUE)            
    def sendTorqueModeDCCurrent(self):
        if self.device.isConnected:
            self.device.sendTorqueType(SimpleFOCDevice.DC_CURRENT_TORQUE)
    def sendTorqueModeFOCCurrent(self):
        if self.device.isConnected:
            self.device.sendTorqueType(SimpleFOCDevice.FOC_CURRENT_TORQUE)

    def commandResponseReceived(self, cmdRespose):
        self.setTorqueMode(self.device.torqueType)