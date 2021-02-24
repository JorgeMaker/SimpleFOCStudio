#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets, QtCore
from src.gui.sharedcomnponets.sharedcomponets import ConfigQLineEdit
from src.simpleFOCConnector import SimpleFOCDevice

class PidGroupBox(QtWidgets.QGroupBox):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setMaximumWidth(300)

        onlyFloatInputValidator = QtGui.QRegExpValidator(
            QtCore.QRegExp("[+-]?([0-9]*[.])?[0-9]+"))

        self.device = SimpleFOCDevice.getInstance()

        self.setObjectName('pidConfigurator')
        self.setTitle('PID Controller configuration')

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName('gridLayout')

        self.dgLabel = QtWidgets.QLabel(self)
        self.dgLabel.setObjectName('dgLabel')
        self.dgLabel.setText('Derivative gain')
        self.gridLayout.addWidget(self.dgLabel, 2, 1, 1, 1)

        self.iglabel = QtWidgets.QLabel(self)
        self.iglabel.setObjectName('iglabel')
        self.iglabel.setText('Integral gain')
        self.gridLayout.addWidget(self.iglabel, 1, 1, 1, 1)

        self.pgLabel = QtWidgets.QLabel(self)
        self.pgLabel.setObjectName('pgLabel')
        self.pgLabel.setText('Proportional gain')
        self.gridLayout.addWidget(self.pgLabel, 0, 1, 1, 1)

        self.vrLabel = QtWidgets.QLabel(self)
        self.vrLabel.setObjectName('vrLabel')
        self.vrLabel.setText('Voltage ramp')
        self.gridLayout.addWidget(self.vrLabel, 4, 1, 1, 1)

        self.igLineEdit = ConfigQLineEdit(self)
        self.igLineEdit.setObjectName('igLineEdit')
        self.igLineEdit.setValidator(onlyFloatInputValidator)
        self.igLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.igLineEdit.updateValue.connect(self.sendIntegralGainAction)
        self.gridLayout.addWidget(self.igLineEdit, 1, 2, 1, 1)

        self.dgButton = QtWidgets.QPushButton(self)
        self.dgButton.setObjectName('dgButton')
        self.dgButton.setText('Set D')
        self.dgButton.clicked.connect(self.sendDerivativeGainAction)
        self.gridLayout.addWidget(self.dgButton, 2, 5, 1, 1)

        self.dgLineEdit = ConfigQLineEdit(self)
        self.dgLineEdit.setObjectName('dgLineEdit')
        self.dgLineEdit.setValidator(onlyFloatInputValidator)
        self.dgLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dgLineEdit.updateValue.connect(self.sendDerivativeGainAction)
        self.gridLayout.addWidget(self.dgLineEdit, 2, 2, 1, 1)

        self.pgButton = QtWidgets.QPushButton(self)
        self.pgButton.setObjectName('pgButton')
        self.pgButton.setText('Set P')
        self.pgButton.clicked.connect(self.sendProportionalGainAction)
        self.gridLayout.addWidget(self.pgButton, 0, 5, 1, 1)

        self.pgLineEdit = ConfigQLineEdit(self)
        self.pgLineEdit.setObjectName('pgLineEdit')
        self.pgLineEdit.setValidator(onlyFloatInputValidator)
        self.pgLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.pgLineEdit.updateValue.connect(self.sendProportionalGainAction)
        self.gridLayout.addWidget(self.pgLineEdit, 0, 2, 1, 1)

        self.vrButton = QtWidgets.QPushButton(self)
        self.vrButton.setObjectName('vrButton')
        self.vrButton.setText('Set R')
        self.vrButton.clicked.connect(self.sendVoltageRampAction)
        self.gridLayout.addWidget(self.vrButton, 4, 5, 1, 1)

        self.igButton = QtWidgets.QPushButton(self)
        self.igButton.setObjectName('igButton')
        self.igButton.setText('Set I')
        self.igButton.clicked.connect(self.sendIntegralGainAction)
        self.gridLayout.addWidget(self.igButton, 1, 5, 1, 1)

        self.vrLineEdit = ConfigQLineEdit(self)
        self.vrLineEdit.setObjectName('vrLineEdit')
        self.vrLineEdit.setValidator(onlyFloatInputValidator)
        self.vrLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.vrLineEdit.updateValue.connect(self.sendVoltageRampAction)
        self.gridLayout.addWidget(self.vrLineEdit, 4, 2, 1, 1)

        self.setDerivativeGainAction(self.device.derivativeGainPID)
        self.setProportionalGainAction(self.device.proportionalGainPID)
        self.setIntegralGainAction(self.device.integralGainPID)
        self.setVoltageRampAction(self.device.voltageRampPID)

        self.connectionStateChanged(self.device.isConnected)
        self.device.addConnectionStateListener(self)
        self.device.commProvider.commandDataReceived.connect(self.commandResponseReceived)

    def connectionStateChanged(self, deviceConnected):
        if deviceConnected is True:
            self.enabeUI()
        else:
            self.disableUI()

    def enabeUI(self):
        self.setEnabled(True)

    def disableUI(self):
        self.setEnabled(False)

    def setDerivativeGainAction(self, value):
        self.dgLineEdit.setText(str(value))

    def setProportionalGainAction(self,value):
        self.pgLineEdit.setText(str(value))

    def setIntegralGainAction(self,value):
        self.igLineEdit.setText(str(value))

    def setVoltageRampAction(self, value):
        self.vrLineEdit.setText(str(value))

    def sendDerivativeGainAction(self):
        value = self.dgLineEdit.text()
        value = value.replace(',', '.')
        self.dgLineEdit.setText(value)
        self.device.sendDerivativeGain(value)

    def sendProportionalGainAction(self):
        value = self.pgLineEdit.text()
        value = value.replace(',', '.')
        self.pgLineEdit.setText(value)
        self.device.sendProportionalGain(self.pgLineEdit.text())

    def sendIntegralGainAction(self):
        value = self.igLineEdit.text()
        value = value.replace(',', '.')
        self.igLineEdit.setText(value)
        self.device.sendIntegralGain(self.igLineEdit.text())

    def sendVoltageRampAction(self):
        value = self.vrLineEdit.text()
        value = value.replace(',', '.')
        self.vrLineEdit.setText(value)
        self.device.sendVoltageRamp(self.vrLineEdit.text())

    def commandResponseReceived(self, commandDataReceived):
        if 'PID velocity| P' in commandDataReceived:
            self.pgLineEdit.setText(commandDataReceived.replace('PID velocity| P:', ''))
        elif 'PID velocity| I' in commandDataReceived:
            self.igLineEdit.setText(commandDataReceived.replace('PID velocity| I:', ''))
        elif 'PID velocity| D' in commandDataReceived:
            self.dgLineEdit.setText(commandDataReceived.replace('PID velocity| D:', ''))
        elif 'PID velocity| volt_ramp' in commandDataReceived:
            self.vrLineEdit.setText(commandDataReceived.replace('PID velocity| volt_ramp:', ''))

