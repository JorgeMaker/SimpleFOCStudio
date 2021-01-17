#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtWidgets
from gui.sharedcomponets import GUIToolKit

class CommandLineGroupBox(QtWidgets.QGroupBox):

    def __init__(self, parent=None, simpleFocConn=None):
        """Constructor for ToolsWidget"""
        super().__init__(parent)

        self.device = simpleFocConn

        self.setMaximumHeight(200)
        self.setObjectName("groupBox")
        self.setTitle("Command Line interface")

        self.cmlVerticalLayout = QtWidgets.QVBoxLayout(self)
        self.cmlVerticalLayout.setObjectName("cmlVerticalLayout")

        self.commandLineDisplay = QtWidgets.QTextEdit(self)
        self.commandLineDisplay.setObjectName("commandLineDisplay")
        self.cmlVerticalLayout.addWidget(self.commandLineDisplay)

        self.commandLineDisplay.setReadOnly(True)
        self.commandLineDisplay.setTextColor(QtGui.QColor(3407616))

        self.cmlWidget = QtWidgets.QWidget(self)
        self.cmlWidget.setObjectName("cmlWidget")
        self.cmlHorizontalLayout = QtWidgets.QHBoxLayout(self.cmlWidget)
        self.cmlHorizontalLayout.setObjectName("cmlHorizontalLayout")

        self.commandLineEdit = QtWidgets.QLineEdit(self.cmlWidget)
        self.commandLineEdit.setObjectName("commandLineEdit")
        self.cmlHorizontalLayout.addWidget(self.commandLineEdit)

        self.commandLineEdit.returnPressed.connect(self.sendAction)

        self.sendButton = QtWidgets.QPushButton(self.cmlWidget)
        self.sendButton.setObjectName("sendButton")
        self.sendButton.setText("Send")
        self.sendButton.setIcon(GUIToolKit.getIconByName("send"))
        self.sendButton.clicked.connect(self.sendAction)

        self.cmlHorizontalLayout.addWidget(self.sendButton)

        self.clearButton = QtWidgets.QPushButton(self.cmlWidget)
        self.clearButton.setObjectName("clearButton")
        self.cmlHorizontalLayout.addWidget(self.clearButton)
        self.clearButton.setIcon(GUIToolKit.getIconByName("delete"))
        self.clearButton.clicked.connect(self.clearAction)
        self.clearButton.setText("Clear")

        self.cmlVerticalLayout.addWidget(self.cmlWidget)

        self.device.commProvider.commandDataReceived.connect(self.publishCommandResponseData)

        self.setEnabled(False)
        self.device.addConnectionStateListener(self)

    def deviceConnected(self, deviceConnected):
        if deviceConnected is True:
            self.enabeUI()
            self.publishCommandResponseData("Connected: Ready to plot")
        else:
            self.disableUI()
            self.publishCommandResponseData("Disconnected ...")

    def enabeUI(self):
        self.setEnabled(True)

    def disableUI(self):
        self.setEnabled(False)

    def publishCommandResponseData(self, data):
        self.commandLineDisplay.append(data)
        self.commandLineDisplay.moveCursor(QtGui.QTextCursor.End)

    def clearAction(self):
        self.commandLineDisplay.setPlainText("")

    def sendAction(self):
        self.device.sendCommand(self.commandLineEdit.text())
        self.commandLineEdit.setText("")
