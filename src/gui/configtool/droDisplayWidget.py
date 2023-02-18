#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import (QtGui,QtWidgets)

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
        self.signal0Label.setObjectName('angleLabel')
        self.signal0Label.setText('Angle')
        self.droHorizontalLayout.addWidget(self.signal0Label)

        self.signal0LCDNumber = QtWidgets.QLCDNumber(self)
        self.putStyleToLCDNumber(self.signal0LCDNumber)
        self.signal0LCDNumber.setObjectName('signal0LCDNumber')
        self.droHorizontalLayout.addWidget(self.signal0LCDNumber)

        self.signal1Label = QtWidgets.QLabel(self)
        self.signal1Label.setObjectName('velLabel')
        self.signal1Label.setText('Velocity')
        self.droHorizontalLayout.addWidget(self.signal1Label)

        self.signal1LCDNumber = QtWidgets.QLCDNumber(self)
        self.putStyleToLCDNumber(self.signal1LCDNumber)
        self.signal1LCDNumber.setObjectName('signal1LCDNumber')
        self.droHorizontalLayout.addWidget(self.signal1LCDNumber)

        self.signal2Label = QtWidgets.QLabel(self)
        self.signal2Label.setObjectName('torqueLabel')
        self.signal2Label.setText('Target')
        self.droHorizontalLayout.addWidget(self.signal2Label)

        self.signal2LCDNumber = QtWidgets.QLCDNumber(self)
        self.putStyleToLCDNumber(self.signal2LCDNumber)
        self.signal2LCDNumber.setObjectName('signal2LCDNumber')
        self.droHorizontalLayout.addWidget(self.signal2LCDNumber)

        self.signal3Label = QtWidgets.QLabel(self)
        self.signal3Label.setObjectName('targetLabel')
        self.signal3Label.setText('Target')
        self.droHorizontalLayout.addWidget(self.signal3Label)

        self.signal3LCDNumber = QtWidgets.QLCDNumber(self)
        self.putStyleToLCDNumber(self.signal3LCDNumber)
        self.signal3LCDNumber.setObjectName('signal3LCDNumber')
        self.droHorizontalLayout.addWidget(self.signal3LCDNumber)

        self.commandResponseReceived('init')

        self.initDiplay()
        self.disableUI()

        self.device.addConnectionStateListener(self)
        self.device.commProvider.stateMonitorReceived.connect(self.commandResponseReceived)

        self.connectionStateChanged(self.device.isConnected)

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
        self.signal3LCDNumber.display(0.0)

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

    def commandResponseReceived(self, cmdRespose):        
        if self.device.torqueType ==  SimpleFOCDevice.VOLTAGE_TORQUE:
            self.signal2Label.setText("Voltage")
            self.signal2LCDNumber.display(self.device.voltageQNow)
        else: # dc current or FOC current
            self.signal2Label.setText("Current")
            self.signal2LCDNumber.display(self.device.currentQNow)

        self.signal3LCDNumber.display(self.device.targetNow)
        self.signal1LCDNumber.display(self.device.velocityNow)
        self.signal0LCDNumber.display(self.device.angleNow)
