#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from src.gui.configtool.connectionControl import ConnectionControlGroupBox
from src.gui.configtool.controlLoopConfig import ControlLoopGroupBox
from src.gui.configtool.deviceJoggingControl import DeviceJoggingControl
from src.gui.configtool.droDisplayWidget import DROGroupBox
from src.gui.configtool.generalControls import GeneralControls
from src.gui.configtool.generalSettingsWidget import GeneralSettingsGroupBox
from src.gui.configtool.graphicWidget import SimpleFOCGraphicWidget
from src.gui.configtool.pidConfiguration import PidGroupBox
from src.gui.configtool.torqueConfig import TorqueGroupBox
from src.gui.sharedcomnponets.commandLineInterface import CommandLineWidget
from src.gui.sharedcomnponets.sharedcomponets import (WorkAreaTabWidget,
                                                      GUIToolKit)
from src.simpleFOCConnector import SimpleFOCDevice


class DeviceConfigurationTool(WorkAreaTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.device = SimpleFOCDevice.getInstance()

        self.setObjectName('DeviceConfigurationTool')

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName('verticalLayout')

        self.counterWidget = QtWidgets.QWidget(self)
        self.counterWidget.setObjectName('counterWidget')
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.counterWidget)
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.digitalReadOut = DROGroupBox(self.counterWidget)
        self.horizontalLayout.addWidget(self.digitalReadOut)
        
        self.controlLoop = ControlLoopGroupBox(self.counterWidget)
        self.horizontalLayout.addWidget(self.controlLoop)

        self.torqueConfig = TorqueGroupBox(self.counterWidget)
        self.horizontalLayout.addWidget(self.torqueConfig)

        self.connectionControl = ConnectionControlGroupBox(self.counterWidget)
        self.horizontalLayout.addWidget(self.connectionControl)
        self.verticalLayout.addWidget(self.counterWidget)

        self.graphicWidget = SimpleFOCGraphicWidget()
        self.verticalLayout.addWidget(self.graphicWidget)

        self.bottomWidget = QtWidgets.QWidget(self)
        self.bottomWidget.setObjectName('bottomWidget')

        self.bottomHorizontalLayout = QtWidgets.QHBoxLayout(self.bottomWidget)
        self.bottomHorizontalLayout.setObjectName('configureHorizontalLayout')

        self.pidConfigurator = PidGroupBox(self.bottomWidget)
        self.bottomHorizontalLayout.addWidget(self.pidConfigurator)

        self.generalLayout = QtWidgets.QVBoxLayout()
        self.generalDeviceSettings = GeneralSettingsGroupBox(self.bottomWidget)

        self.generalControls = GeneralControls(self.bottomWidget)
        self.generalLayout.addWidget(self.generalControls)
        self.generalLayout.addWidget(self.generalDeviceSettings)
        self.bottomHorizontalLayout.addLayout(self.generalLayout)

        self.lasWidget = QtWidgets.QWidget(self)
        self.lastVerticalLayout = QtWidgets.QVBoxLayout(self.lasWidget)

        self.commandLine = CommandLineWidget(self)
        self.lastVerticalLayout.addWidget(self.commandLine)

        self.joggingControl = DeviceJoggingControl(self)
        self.lastVerticalLayout.addWidget(self.joggingControl)

        self.bottomHorizontalLayout.addWidget(self.lasWidget)
        self.verticalLayout.addWidget(self.bottomWidget)

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
