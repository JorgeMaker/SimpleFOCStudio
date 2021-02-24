#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from PyQt5 import QtGui, QtWidgets

from src.gui.sharedcomnponets.sharedcomponets import GUIToolKit
from src.simpleFOCConnector import SimpleFOCDevice


class DROGroupBox(QtWidgets.QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.device = SimpleFOCDevice.getInstance()

        self.setTitle('Simple FOC Digital Read Out')
        self.setObjectName('digitalReadOut')

        self.droHorizontalLayout = QtWidgets.QHBoxLayout(self)
        self.droHorizontalLayout.setObjectName('droHorizontalLayout')

        self.signal0Label = QtWidgets.QLabel(self)
        self.signal0Label.setObjectName('signal0Label')
        self.signal0Label.setText('Signal 0')
        self.droHorizontalLayout.addWidget(self.signal0Label)

        self.signal0LCDNumber = QtWidgets.QLCDNumber(self)
        self.putStyleToLCDNumber(self.signal0LCDNumber)
        self.signal0LCDNumber.setObjectName('signal0LCDNumber')
        self.droHorizontalLayout.addWidget(self.signal0LCDNumber)

        self.signal1Label = QtWidgets.QLabel(self)
        self.signal1Label.setObjectName('signal1Label')
        self.signal1Label.setText('Signal 1')
        self.droHorizontalLayout.addWidget(self.signal1Label)

        self.signal1LCDNumber = QtWidgets.QLCDNumber(self)
        self.putStyleToLCDNumber(self.signal1LCDNumber)
        self.signal1LCDNumber.setObjectName('signal1LCDNumber')
        self.droHorizontalLayout.addWidget(self.signal1LCDNumber)

        self.signal2Label = QtWidgets.QLabel(self)
        self.signal2Label.setObjectName('voltageLable')
        self.signal2Label.setText('Signal 2')
        self.droHorizontalLayout.addWidget(self.signal2Label)

        self.signal2LCDNumber = QtWidgets.QLCDNumber(self)
        self.putStyleToLCDNumber(self.signal2LCDNumber)
        self.signal2LCDNumber.setObjectName('signal2LCDNumber')
        self.droHorizontalLayout.addWidget(self.signal2LCDNumber)

        self.device.commProvider.telemetryDataReceived.connect(self.updateDRO)

        self.controlTypeChonged(self.device.controlType)

        self.initDiplay()
        self.disableUI()

        self.device.addConnectionStateListener(self)
        self.device.commProvider.commandDataReceived.connect(
            self.commandResponseReceived)

        self.connectionStateChanged(self.device.isConnected)

    def updateLabels(self, label0, label1, label2):
        self.signal0Label.setText(label0)
        self.signal1Label.setText(label1)
        self.signal2Label.setText(label2)

    def connectionStateChanged(self, isConnectedFlag):
        if isConnectedFlag is True:
            self.enabeUI()
            self.initDiplay()
        else:
            self.initDiplay()
            self.disableUI()

    def enabeUI(self):
        self.setEnabled(True)

    def disableUI(self):
        self.setEnabled(False)

    def initDiplay(self):
        self.signal0LCDNumber.display(0.0)
        self.signal1LCDNumber.display(0.0)
        self.signal2LCDNumber.display(0.0)

    def putStyleToLCDNumber(self, lcdNumber):
        lcdNumber.setStyleSheet('''QLCDNumber {background-color: white;}''')
        palette = self.setColor(lcdNumber.palette(), GUIToolKit.RED_COLOR)
        lcdNumber.setPalette(palette)

    def setColor(self, palette, colorTouple):
        R = colorTouple[0]
        G = colorTouple[1]
        B = colorTouple[2]
        # foreground color
        palette.setColor(palette.WindowText, QtGui.QColor(R, G, B))
        # background color
        palette.setColor(palette.Background, QtGui.QColor(R, G, B))
        # 'light' border
        palette.setColor(palette.Light, QtGui.QColor(R, G, B))
        # 'dark' border
        palette.setColor(palette.Dark, QtGui.QColor(R, G, B))
        return palette

    def setValues(self, values):
        self.signal0LCDNumber.display(values[0])
        self.signal1LCDNumber.display(values[1])
        self.signal2LCDNumber.display(values[2])

    def updateDRO(self, signal0, signal1, signal2):
        try:
            if type(signal0) is float and type(signal1) is float and type(
                    signal2) is float:
                self.signal0LCDNumber.display(signal0)
                self.signal2LCDNumber.display(signal1)
                self.signal1LCDNumber.display(signal2)
        except IndexError as error:
            logging.error(error, exc_info=True)

    def controlTypeChonged(self, controlMode):
        label0, label1, label2 = SimpleFOCDevice.getSignalLabels(controlMode)
        self.updateLabels(label0, label1, label2)

    def commandResponseReceived(self, cmdRespose):
        if 'Control: ' in cmdRespose:
            self.controlTypeChonged(SimpleFOCDevice.getControlModeCode(
                cmdRespose.replace('Control: ', '')))
