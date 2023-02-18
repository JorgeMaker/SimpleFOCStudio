#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
from PyQt5 import (QtGui, QtCore, QtWidgets)

from src.gui.sharedcomnponets.sharedcomponets import GUIToolKit
from src.gui.sharedcomnponets.sharedcomponets import SerialPortComboBox
from src.simpleFOCConnector import SimpleFOCDevice


class ConfigureConnection(QtWidgets.QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.device = SimpleFOCDevice.getInstance()

        self.setTitle('Configure serial connection')
        self.setObjectName('configureConnection')

        self.configCoonLayout = QtWidgets.QHBoxLayout(self)
        self.configCoonLayout.setObjectName(
            'configureConnectionorizontalLayout')

        self.portNameLabel = QtWidgets.QLabel(self)
        self.portNameLabel.setObjectName('portNameLabel')
        self.configCoonLayout.addWidget(self.portNameLabel)

        self.portNameComboBox = SerialPortComboBox(self)
        self.portNameComboBox.setObjectName('portNameComboBox')
        self.portNameComboBox.setMinimumWidth(250)
        self.configCoonLayout.addWidget(self.portNameComboBox)

        self.bitRateLabel = QtWidgets.QLabel(self)
        self.bitRateLabel.setObjectName('bitRateLabel')
        self.configCoonLayout.addWidget(self.bitRateLabel)

        self.bitRatelineEdit = QtWidgets.QLineEdit(self)
        self.bitRatelineEdit.setObjectName('bitRatelineEdit')
        self.bitRatelineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]*$")))
        self.bitRatelineEdit.setText('115200')
        self.configCoonLayout.addWidget(self.bitRatelineEdit)

        self.parityLabel = QtWidgets.QLabel(self)
        self.parityLabel.setObjectName('parityLabel')
        self.configCoonLayout.addWidget(self.parityLabel)

        self.parityComboBox = QtWidgets.QComboBox(self)
        self.parityComboBox.setObjectName('parityComboBox')
        self.parityComboBox.addItems(serial.PARITY_NAMES.values())
        self.configCoonLayout.addWidget(self.parityComboBox)

        serial.PARITY_NAMES.values()

        self.byteSizeLabel = QtWidgets.QLabel(self)
        self.byteSizeLabel.setObjectName('byteSizeLabel')
        self.configCoonLayout.addWidget(self.byteSizeLabel)

        self.byteSizeComboBox = QtWidgets.QComboBox(self)
        self.byteSizeComboBox.setObjectName('byteSizeComboBox')
        byteSizeList = [str(serial.EIGHTBITS), str(serial.FIVEBITS),
                        str(serial.SIXBITS),
                        str(serial.SEVENBITS)]
        self.byteSizeComboBox.addItems(byteSizeList)
        self.configCoonLayout.addWidget(self.byteSizeComboBox)

        self.stopBitsLabel = QtWidgets.QLabel(self)
        self.stopBitsLabel.setObjectName('stopBitsLabel')
        self.configCoonLayout.addWidget(self.stopBitsLabel)

        self.stopBitsComboBox = QtWidgets.QComboBox(self)
        byteStopBitsList = [str(serial.STOPBITS_ONE),
                            str(serial.STOPBITS_ONE_POINT_FIVE),
                            str(serial.STOPBITS_TWO)]
        self.stopBitsComboBox.addItems(byteStopBitsList)
        self.stopBitsComboBox.setObjectName('stopBitsComboBox')
        self.configCoonLayout.addWidget(self.stopBitsComboBox)

        self.connectDisconnectButton = QtWidgets.QPushButton(self)
        self.connectDisconnectButton.setIcon(
            GUIToolKit.getIconByName('connect'))
        self.connectDisconnectButton.setObjectName('connectDeviceButton')
        self.connectDisconnectButton.setText('Connect')
        self.connectDisconnectButton.clicked.connect(
            self.connectDisconnectDeviceAction)

        self.configCoonLayout.addWidget(self.connectDisconnectButton)

        self.portNameLabel.setText('Port Name')
        self.bitRateLabel.setText('Bit rate')
        self.parityLabel.setText('Parity')
        self.byteSizeLabel.setText('Byte size')
        self.stopBitsLabel.setText('Stop bits')

        self.device.addConnectionStateListener(self)
        self.connectionStateChanged(self.device.isConnected)

    def getConfigValues(self):
        values = {
            'connectionID': '',
            'serialPortName': self.portNameComboBox.currentText(),
            'serialRate': self.bitRatelineEdit.text(),
            'stopBits': self.stopBitsExtractor(self.stopBitsComboBox.currentText()),
            'serialByteSize': int(str(self.byteSizeComboBox.currentText())),
            'serialParity':  list(serial.PARITY_NAMES.keys())[list(serial.PARITY_NAMES.values()).index(self.parityComboBox.currentText())][0]
        }
        return values

    def stopBitsExtractor(self, value):
        if value == '1.5':
            return float(self.stopBitsComboBox.currentText())
        else:
            return int(self.stopBitsComboBox.currentText())

    def connectionStateChanged(self, isConnectedFlag):
        if isConnectedFlag:
            self.connectDisconnectButton.setText('Disconnect')
            self.connectDisconnectButton.setIcon(
                GUIToolKit.getIconByName('disconnect'))
        else:
            self.connectDisconnectButton.setText('Connect')
            self.connectDisconnectButton.setIcon(
                GUIToolKit.getIconByName('connect'))

        self.portNameLabel.setEnabled(not isConnectedFlag)
        self.portNameComboBox.setEnabled(not isConnectedFlag)
        self.bitRateLabel.setEnabled(not isConnectedFlag)
        self.bitRatelineEdit.setEnabled(not isConnectedFlag)
        self.parityLabel.setEnabled(not isConnectedFlag)
        self.parityComboBox.setEnabled(not isConnectedFlag)
        self.byteSizeLabel.setEnabled(not isConnectedFlag)
        self.byteSizeComboBox.setEnabled(not isConnectedFlag)
        self.stopBitsLabel.setEnabled(not isConnectedFlag)
        self.stopBitsComboBox.setEnabled(not isConnectedFlag)

    def connectDisconnectDeviceAction(self):
        if self.device.isConnected:
            self.disConnectAction()
        else:
            self.connectAction()

    def connectAction(self):
        deviceConfig = self.getConfigValues()
        self.device.configureConnection(deviceConfig)
        self.device.connect(SimpleFOCDevice.ONLY_CONNECT)

    def disConnectAction(self):
        self.device.disConnect()