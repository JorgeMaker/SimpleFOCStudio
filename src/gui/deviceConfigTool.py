#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets

from gui.controlLopConfig import ControlLoopGroupBox
from gui.generalSettingsWidget import GeneralSettingsGroupBox
from gui.connectionControl import ConnectionControlGroupBox
from gui.droDisplayWidget import DROGroupBox
from gui.commandLineInterface import CommandLineGroupBox
from gui.pidConfiguration import PidGroupBox
from gui.graphicWidget import SimpleFOCGraphicWidget
from simpleFOCConnector import SimpleFOCDevice

class DeviceConfigurationWidget(QtWidgets.QWidget):

    def __init__(self, parent=None,simpleFocConn=None):
        """Constructor for ToolsWidget"""
        super().__init__(parent)

        self.device = simpleFocConn

        if simpleFocConn is None:
            self.device = SimpleFOCDevice()

        self.setObjectName("DeviceConfigurationTool")

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.counterWidget = QtWidgets.QWidget(self)
        self.counterWidget.setObjectName("counterWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.counterWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.digitalReadOutGroupBox = DROGroupBox(self.counterWidget,
                                                  simpleFocConn=self.device)
        self.horizontalLayout.addWidget(self.digitalReadOutGroupBox)

        self.controlLoopGroupBox = ControlLoopGroupBox(self.counterWidget,simpleFocConn=self.device)
        self.horizontalLayout.addWidget(self.controlLoopGroupBox)

        self.generalControlGroupBox = ConnectionControlGroupBox(self.counterWidget, simpleFocConn=self.device)
        self.horizontalLayout.addWidget(self.generalControlGroupBox)
        self.verticalLayout.addWidget(self.counterWidget)

        self.graphicWidget = SimpleFOCGraphicWidget(simpleFocConn=self.device)
        self.verticalLayout.addWidget(self.graphicWidget)

        self.bottomWidget = QtWidgets.QWidget(self)
        self.bottomWidget.setObjectName("bottomWidget")

        self.bottomHorizontalLayout = QtWidgets.QHBoxLayout(self.bottomWidget)
        self.bottomHorizontalLayout.setObjectName("configureHorizontalLayout")


        self.pidGroupBox = PidGroupBox(self.bottomWidget,simpleFocConn=self.device)
        self.bottomHorizontalLayout.addWidget(self.pidGroupBox)

        self.generalDeviceSettingsGroupBox = GeneralSettingsGroupBox(self.bottomWidget,simpleFocConn=self.device)
        self.bottomHorizontalLayout.addWidget(self.generalDeviceSettingsGroupBox)

        self.commandLineGroupBox = CommandLineGroupBox(self,simpleFocConn=self.device)
        self.bottomHorizontalLayout.addWidget(self.commandLineGroupBox)

        self.verticalLayout.addWidget(self.bottomWidget)

    def connectDevice(self):
        self.device.connect()

    def disConnectDevice(self):
        self.device.disConnect()

    def configureConnection(self, configvalues):
        self.device.serialPortName = configvalues["serialPortName"]
        self.device.serialRate = configvalues["serialRate"]
        self.device.stopBits = configvalues["stopBits"]
        self.device.serialByteSize = configvalues["serialByteSize"]
        self.device.serialParity = configvalues["serialParity"]



