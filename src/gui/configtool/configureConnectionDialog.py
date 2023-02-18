#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
from PyQt5 import (QtCore, QtGui, QtWidgets)

from src.gui.sharedcomnponets.sharedcomponets import SerialPortComboBox
from src.simpleFOCConnector import SimpleFOCDevice


class ConfigureSerailConnectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(SimpleFOCDevice.getInstance())

    def setupUi(self, device=None):
        self.setObjectName('Dialog')
        self.resize(700, 188)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName('gridLayout')

        self.portNameLabel = QtWidgets.QLabel(self)
        self.portNameLabel.setObjectName('portNameLabel')
        self.gridLayout.addWidget(self.portNameLabel, 0, 0, 1, 1)

        self.portNameComboBox = SerialPortComboBox(self)
        self.portNameComboBox.setObjectName('portNameComboBox')
        self.portNameComboBox.setMinimumWidth(250)
        self.gridLayout.addWidget(self.portNameComboBox, 0, 1, 1, 1)

        self.bitRateLabel = QtWidgets.QLabel(self)
        self.bitRateLabel.setObjectName('bitRateLabel')
        self.gridLayout.addWidget(self.bitRateLabel, 0, 2, 1, 1)



        self.bitRatelineEdit = QtWidgets.QLineEdit(self)
        self.bitRatelineEdit.setObjectName('bitRatelineEdit')
        self.bitRatelineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]*$")))
        self.gridLayout.addWidget(self.bitRatelineEdit, 0, 3, 1, 1)

        self.parityLabel = QtWidgets.QLabel(self)
        self.parityLabel.setObjectName('parityLabel')
        self.gridLayout.addWidget(self.parityLabel, 1, 0, 1, 1)

        self.parityComboBox = QtWidgets.QComboBox(self)
        self.parityComboBox.setObjectName('parityComboBox')
        self.parityComboBox.addItems(serial.PARITY_NAMES.values())
        self.gridLayout.addWidget(self.parityComboBox, 1, 1, 1, 1)

        serial.PARITY_NAMES.values()

        self.byteSizeLabel = QtWidgets.QLabel(self)
        self.byteSizeLabel.setObjectName('byteSizeLabel')
        self.gridLayout.addWidget(self.byteSizeLabel, 1, 2, 1, 1)

        self.byteSizeComboBox = QtWidgets.QComboBox(self)
        self.byteSizeComboBox.setObjectName('byteSizeComboBox')
        byteSizeList = [str(serial.EIGHTBITS), str(serial.FIVEBITS), str(serial.SIXBITS),
                        str(serial.SEVENBITS)]
        self.byteSizeComboBox.addItems(byteSizeList)
        self.gridLayout.addWidget(self.byteSizeComboBox, 1, 3, 1, 1)

        self.stopBitsLabel = QtWidgets.QLabel(self)
        self.stopBitsLabel.setObjectName('stopBitsLabel')
        self.gridLayout.addWidget(self.stopBitsLabel, 2, 0, 1, 1)

        self.stopBitsComboBox = QtWidgets.QComboBox(self)
        byteStopBitsList = [str(serial.STOPBITS_ONE),
                            str(serial.STOPBITS_ONE_POINT_FIVE),
                            str(serial.STOPBITS_TWO)]
        self.stopBitsComboBox.addItems(byteStopBitsList)
        self.stopBitsComboBox.setObjectName('stopBitsComboBox')
        self.gridLayout.addWidget(self.stopBitsComboBox, 2, 1, 1, 1)

        self.connectionIDLabel = QtWidgets.QLabel(self)
        self.connectionIDLabel.setObjectName('connectionNameLabel')
        self.gridLayout.addWidget(self.connectionIDLabel, 2, 2, 1, 1)

        self.connectionIDlineEdit = QtWidgets.QLineEdit(self)
        self.connectionIDlineEdit.setMaxLength(10)
        self.connectionIDlineEdit.setObjectName('connectionNameEdit')
        self.gridLayout.addWidget(self.connectionIDlineEdit, 2, 3, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName('buttonBox')

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 4)

        self.setWindowTitle('Configure serial connection')
        self.portNameLabel.setText('Port Name')
        self.bitRateLabel.setText('Bit rate')
        self.parityLabel.setText('Parity')
        self.byteSizeLabel.setText('Byte size')
        self.stopBitsLabel.setText('Stop bits')
        self.connectionIDLabel.setText('Conn ID')

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        QtCore.QMetaObject.connectSlotsByName(self)

        if device is not None:
            self.fillForm(device)

    def fillForm(self, deviceConnector):
        self.connectionIDlineEdit.setText(deviceConnector.connectionID)
        self.portNameComboBox.setCurrentText(deviceConnector.serialPortName)
        self.bitRatelineEdit.setText(str(deviceConnector.serialRate))
        self.stopBitsComboBox.setCurrentText(str(deviceConnector.stopBits))
        self.byteSizeComboBox.setCurrentText(str(deviceConnector.serialByteSize))
        self.parityComboBox.setCurrentText(str(deviceConnector.serialParity))

    def getConfigValues(self):
        values = {
            'connectionID': self.connectionIDlineEdit.text(),
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