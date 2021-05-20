#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from src.gui.commandlinetool.configureConnectionWidget import \
    ConfigureConnection
from src.gui.sharedcomnponets.commandLineInterface import CommandLineWidget
from src.gui.sharedcomnponets.sharedcomponets import (WorkAreaTabWidget,
                                                      GUIToolKit)
from src.simpleFOCConnector import SimpleFOCDevice


class CommandLineConsoleTool(WorkAreaTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.device = SimpleFOCDevice.getInstance()

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName('verticalLayout')

        self.configureConnection = ConfigureConnection()
        self.verticalLayout.addWidget(self.configureConnection)

        self.commandLineInterface = CommandLineWidget()
        self.verticalLayout.addWidget(self.commandLineInterface)

        self.device.commProvider.rawDataReceived.connect(self.commandLineInterface.publishCommandResponseData)

    def getTabIcon(self):
        return GUIToolKit.getIconByName('consoletool')

    def getTabName(self):
        return self.device.connectionID
