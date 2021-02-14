#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from src.gui.configtool.controlLoopConfig import ControlLoopGroupBox
from src.gui.configtool.generalSettingsWidget import GeneralSettingsGroupBox
from src.gui.configtool.connectionControl import ConnectionControlGroupBox
from src.gui.configtool.droDisplayWidget import DROGroupBox
from src.gui.sharedcomnponets.commandLineInterface import CommandLineGroupBox
from src.gui.configtool.pidConfiguration import PidGroupBox
from src.gui.configtool.graphicWidget import SimpleFOCGraphicWidget
from src.gui.sharedcomnponets.sharedcomponets import (WorkAreaTabWidget, GUIToolKit)

class DeviceConfigurationWidget(WorkAreaTabWidget):

    def __init__(self, parent=None,simpleFocConn=None):
        super().__init__(parent)

        self.device = simpleFocConn

        self.setObjectName('DeviceConfigurationTool')

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName('verticalLayout')

        self.counterWidget = QtWidgets.QWidget(self)
        self.counterWidget.setObjectName('counterWidget')
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.counterWidget)
        self.horizontalLayout.setObjectName('horizontalLayout')

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
        self.bottomWidget.setObjectName('bottomWidget')

        self.bottomHorizontalLayout = QtWidgets.QHBoxLayout(self.bottomWidget)
        self.bottomHorizontalLayout.setObjectName('configureHorizontalLayout')


        self.pidGroupBox = PidGroupBox(self.bottomWidget,simpleFocConn=self.device)
        self.bottomHorizontalLayout.addWidget(self.pidGroupBox)

        self.generalDeviceSettingsGroupBox = GeneralSettingsGroupBox(self.bottomWidget,simpleFocConn=self.device)
        self.bottomHorizontalLayout.addWidget(self.generalDeviceSettingsGroupBox)

        self.commandLineGroupBox = CommandLineGroupBox(self,simpleFocConn=self.device)

        self.bottomHorizontalLayout.addWidget(self.commandLineGroupBox)

        self.verticalLayout.addWidget(self.bottomWidget)

        self.device.commProvider.commandDataReceived.connect(self.commandLineGroupBox.publishCommandResponseData)



    def connectDevice(self):
        self.device.connect()

    def disConnectDevice(self):
        self.device.disConnect()

    def getTabIcon(self):
        return GUIToolKit.getIconByName('motor')

    def getTabName(self):
        return self.device.connectionID


    def configureConnection(self, configvalues):
        self.device.serialPortName = configvalues['serialPortName']
        self.device.serialRate = configvalues['serialRate']
        self.device.stopBits = configvalues['stopBits']
        self.device.serialByteSize = configvalues['serialByteSize']
        self.device.serialParity = configvalues['serialParity']

