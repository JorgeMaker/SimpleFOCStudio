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


        
        self.selectorTorque = QtWidgets.QComboBox(self)
        self.selectorTorque.setObjectName('selectorControlLoop')
        self.selectorTorque.addItems(['Voltage', 'DC Current', 'FOC Current'])
        self.selectorTorque.currentIndexChanged.connect(self.changeTorque)
        self.torqueTypeHorizontalLayout.addWidget(self.selectorTorque)

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
            self.selectorTorque.setCurrentIndex(0)
        elif value == SimpleFOCDevice.DC_CURRENT_TORQUE:
            self.selectorTorque.setCurrentIndex(1)
        elif value == SimpleFOCDevice.FOC_CURRENT_TORQUE:
            self.selectorTorque.setCurrentIndex(2)

    def changeTorque(self):
        index = self.selectorTorque.currentIndex()
        if index == 0:
            self.device.sendTorqueType(SimpleFOCDevice.VOLTAGE_TORQUE)
        elif index == 1:
            self.device.sendTorqueType(SimpleFOCDevice.DC_CURRENT_TORQUE)
        elif index == 2:
            self.device.sendTorqueType(SimpleFOCDevice.FOC_CURRENT_TORQUE)

    def commandResponseReceived(self, cmdRespose):
        self.setTorqueMode(self.device.torqueType)