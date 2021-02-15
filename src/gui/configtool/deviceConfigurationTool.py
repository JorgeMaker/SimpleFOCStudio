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

class DeviceConfigurationTool(WorkAreaTabWidget):

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
        self.digitalReadOut = DROGroupBox(self.counterWidget, simpleFocConn=self.device)
        self.horizontalLayout.addWidget(self.digitalReadOut)

        self.controlLoop = ControlLoopGroupBox(self.counterWidget, simpleFocConn=self.device)
        self.horizontalLayout.addWidget(self.controlLoop)

        self.connectionControl = ConnectionControlGroupBox(self.counterWidget, simpleFocConn=self.device)
        self.horizontalLayout.addWidget(self.connectionControl)
        self.verticalLayout.addWidget(self.counterWidget)

        self.graphicWidget = SimpleFOCGraphicWidget(simpleFocConn=self.device)
        self.verticalLayout.addWidget(self.graphicWidget)

        self.bottomWidget = QtWidgets.QWidget(self)
        self.bottomWidget.setObjectName('bottomWidget')

        self.bottomHorizontalLayout = QtWidgets.QHBoxLayout(self.bottomWidget)
        self.bottomHorizontalLayout.setObjectName('configureHorizontalLayout')

        self.pidConfigurator = PidGroupBox(self.bottomWidget, simpleFocConn=self.device)
        self.bottomHorizontalLayout.addWidget(self.pidConfigurator)

        self.generalDeviceSettings = GeneralSettingsGroupBox(self.bottomWidget, simpleFocConn=self.device)
        self.bottomHorizontalLayout.addWidget(self.generalDeviceSettings)

        self.commandLine = CommandLineGroupBox(self, simpleFocConn=self.device)
        self.bottomHorizontalLayout.addWidget(self.commandLine)
        self.verticalLayout.addWidget(self.bottomWidget)

        self.device.addConnectionStateListener(self.commandLine)
        self.device.commProvider.commandDataReceived.connect(self.commandLine.publishCommandResponseData)

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
