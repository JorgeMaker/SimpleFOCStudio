#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import (QtGui, QtWidgets, QtCore)

from src.gui.sharedcomnponets.sharedcomponets import GUIToolKit
from src.simpleFOCConnector import SimpleFOCDevice


class DeviceJoggingControl(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.device = SimpleFOCDevice.getInstance()

        self.setObjectName('joggingControl')
        self.setTitle('Jogging control')

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName('generalControlHL')

        self.fastFordwardButton = QtWidgets.QPushButton()
        self.fastFordwardButton.setObjectName('fastbackward')
        self.fastFordwardButton.setIcon(GUIToolKit.getIconByName('fastbackward'))
        self.fastFordwardButton.clicked.connect(self.joggingFastBackward)
        self.horizontalLayout.addWidget(self.fastFordwardButton)

        self.backwardButton = QtWidgets.QPushButton()
        self.backwardButton.setObjectName('backward')
        self.backwardButton.setIcon(GUIToolKit.getIconByName('backward'))
        self.backwardButton.clicked.connect(self.joggingBackward)
        self.horizontalLayout.addWidget(self.backwardButton)

        self.stopButton = QtWidgets.QPushButton()
        self.stopButton.setObjectName('stopbutton')
        self.stopButton.setIcon(GUIToolKit.getIconByName('stopjogging'))
        self.stopButton.clicked.connect(self.joggingStop)
        self.horizontalLayout.addWidget(self.stopButton)

        self.fordwardButton = QtWidgets.QPushButton()
        self.fordwardButton.setObjectName('fordward')
        self.fordwardButton.setIcon(GUIToolKit.getIconByName('fordward'))
        self.fordwardButton.clicked.connect(self.joggingFordward)
        self.horizontalLayout.addWidget(self.fordwardButton)

        self.fastBackwardButton = QtWidgets.QPushButton()
        self.fastBackwardButton.setObjectName('fastfordward')
        self.fastBackwardButton.setIcon(GUIToolKit.getIconByName('fastfordward'))
        self.fastBackwardButton.clicked.connect(self.joggingfastFordward)
        self.horizontalLayout.addWidget(self.fastBackwardButton)

        self.incrementLabel = QtWidgets.QLabel("Increment:")
        self.horizontalLayout.addWidget(self.incrementLabel)

        onlyFloat = QtGui.QRegExpValidator(
            QtCore.QRegExp("[+-]?([0-9]*[.])?[0-9]+"))
        self.incrementEdit = QtWidgets.QLineEdit()
        self.incrementEdit.setValidator(onlyFloat)
        self.incrementEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.incrementEdit.setText('1.0')
        self.incrementEdit.setObjectName('incrementEdit')
        self.horizontalLayout.addWidget(self.incrementEdit)

        self.disableUI()
        self.device.addConnectionStateListener(self)

    def connectionStateChanged(self, isConnectedFlag):
        if isConnectedFlag is True:
            self.enabeUI()
        else:
            self.disableUI()
    def enabeUI(self):
        self.setEnabled(True)

    def disableUI(self):
        self.setEnabled(False)

    def joggingFastBackward(self):
        currenttarget = self.device.targetNow
        increment = self.incrementEdit.text()
        newTarget = float(currenttarget) - 2 * float(increment)
        self.device.sendTargetValue(str(newTarget))
    def joggingBackward(self):
        increment = self.incrementEdit.text()
        currenttarget = self.device.targetNow
        newTarget = float(currenttarget) - float(increment)
        self.device.sendTargetValue(str(newTarget))
    def joggingStop(self):
        controltType = self.device.controlType
        if (controltType == SimpleFOCDevice.ANGLE_CONTROL or
                controltType == SimpleFOCDevice.ANGLE_OPENLOOP_CONTROL):
            self.device.sendTargetValue(self.device.angleNow)
        if (controltType == SimpleFOCDevice.VELOCITY_CONTROL or
                controltType == SimpleFOCDevice.VELOCITY_OPENLOOP_CONTROL):
            self.device.sendTargetValue('0')
    def joggingFordward(self):
        increment = self.incrementEdit.text()
        currenttarget = self.device.targetNow
        newTarget = float(currenttarget) + float(increment)
        self.device.sendTargetValue(str(newTarget))
    def joggingfastFordward(self):
        increment = self.incrementEdit.text()
        currenttarget = self.device.targetNow
        newTarget = float(currenttarget) + 2 * float(increment)
        self.device.sendTargetValue(str(newTarget))