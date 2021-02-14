#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from src.gui.sharedcomnponets.commandLineInterface import CommandLineGroupBox
from src.gui.commandlinetool.configureConnectionWidget import ConfigureConnection
from src.gui.sharedcomnponets.sharedcomponets import (WorkAreaTabWidget, GUIToolKit)

class CommandLineConsoleTool(WorkAreaTabWidget):

    def __init__(self, parent=None,simpleFocConn=None):
        super().__init__(parent)

        self.device = simpleFocConn

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName('verticalLayout')

        self.configureConnectionWidget = ConfigureConnection(simpleFOCConn=self.device)
        self.verticalLayout.addWidget(self.configureConnectionWidget)

        self.commandLineInterface = CommandLineGroupBox(simpleFocConn=self.device)
        self.verticalLayout.addWidget(self.commandLineInterface)

        self.device.commProvider.rawDataReceived.connect(
            self.commandLineInterface.publishCommandResponseData)


    def getTabIcon(self):
        return GUIToolKit.getIconByName('consoletool')

    def getTabName(self):
        return self.device.connectionID
