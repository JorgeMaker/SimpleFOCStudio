#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets, QtCore
from src.gui.sharedcomnponets.sharedcomponets import ConfigQLineEdit
from src.simpleFOCConnector import SimpleFOCDevice

class GeneralSettingsGroupBox(QtWidgets.QGroupBox):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setMaximumWidth(300)

        onlyFloat = QtGui.QRegExpValidator(
            QtCore.QRegExp("[+-]?([0-9]*[.])?[0-9]+"))

        self.device = SimpleFOCDevice.getInstance()

        self.setTitle('General device settings')

        self.setObjectName('generalDeviceSettings')

        self.gcGridLayout = QtWidgets.QGridLayout(self)
        self.gcGridLayout.setObjectName('gcGridLayout')

        self.pGainLabel = QtWidgets.QLabel(self)
        self.pGainLabel.setObjectName('pGainLabel')
        self.pGainLabel.setText('P gain')
        self.gcGridLayout.addWidget(self.pGainLabel, 3, 0, 1, 1)

        self.volLimitLabel = QtWidgets.QLabel(self)
        self.volLimitLabel.setObjectName('volLimitLabel')
        self.volLimitLabel.setText('Voltage limit')
        self.gcGridLayout.addWidget(self.volLimitLabel, 6, 0, 1, 1)

        self.velLimitlabel = QtWidgets.QLabel(self)
        self.velLimitlabel.setObjectName('velLimitlabel')
        self.velLimitlabel.setText('velocity limit')
        self.gcGridLayout.addWidget(self.velLimitlabel, 4, 0, 1, 1)

        self.lpfLabel = QtWidgets.QLabel(self)
        self.lpfLabel.setObjectName('lpfLabel')
        self.lpfLabel.setText('Low pass Filter')
        self.gcGridLayout.addWidget(self.lpfLabel, 2, 0, 1, 1)

        self.lpfLineEdit = ConfigQLineEdit(self)
        self.lpfLineEdit.setObjectName('lpfLineEdit')
        self.lpfLineEdit.setValidator(onlyFloat)
        self.lpfLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lpfLineEdit.updateValue.connect(self.sendLowPassFilterAction)
        self.gcGridLayout.addWidget(self.lpfLineEdit, 2, 1, 1, 1)

        self.pgainLineEdit = ConfigQLineEdit(self)
        self.pgainLineEdit.setObjectName('pgainLineEdit')
        self.pgainLineEdit.setValidator(onlyFloat)
        self.pgainLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.pgainLineEdit.updateValue.connect(self.sendPGainAction)
        self.gcGridLayout.addWidget(self.pgainLineEdit, 3, 1, 1, 1)

        self.vlLineEdit = ConfigQLineEdit(self)
        self.vlLineEdit.setObjectName('vlLineEdit')
        self.vlLineEdit.setValidator(onlyFloat)
        self.vlLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.vlLineEdit.updateValue.connect(self.sendVelLimitAction)
        self.gcGridLayout.addWidget(self.vlLineEdit, 4, 1, 1, 1)

        self.volLLineEdit = ConfigQLineEdit(self)
        self.volLLineEdit.setObjectName('volLLineEdit')
        self.volLLineEdit.setValidator(onlyFloat)
        self.volLLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.volLLineEdit.updateValue.connect(self.sendVoltageLimitAction)
        self.gcGridLayout.addWidget(self.volLLineEdit, 6, 1, 1, 1)

        self.lpfButton = QtWidgets.QPushButton(self)
        self.lpfButton.setObjectName('lpfButton')
        self.lpfButton.setText('Set F')
        self.lpfButton.clicked.connect(self.sendLowPassFilterAction)
        self.gcGridLayout.addWidget(self.lpfButton, 2, 2, 1, 1)

        self.pGainButton = QtWidgets.QPushButton(self)
        self.pGainButton.setObjectName('pGainButton')
        self.pGainButton.setText('Set K')
        self.pGainButton.clicked.connect(self.sendPGainAction)
        self.gcGridLayout.addWidget(self.pGainButton, 3, 2, 1, 1)

        self.velLimitButton = QtWidgets.QPushButton(self)
        self.velLimitButton.setObjectName('velLimitButton')
        self.velLimitButton.setText('Set N')
        self.velLimitButton.clicked.connect(self.sendVelLimitAction)
        self.gcGridLayout.addWidget(self.velLimitButton, 4, 2, 1, 1)

        self.voltageLimitButton = QtWidgets.QPushButton( self)
        self.voltageLimitButton.setObjectName('VoltageLimitButton')
        self.voltageLimitButton.setText('Set L')
        self.voltageLimitButton.clicked.connect(self.sendVoltageLimitAction)
        self.gcGridLayout.addWidget(self.voltageLimitButton, 6, 2, 1, 1)

        self.setLowPassFilter(self.device.lowPassFilter)
        self.setPGain(self.device.anglePGain)
        self.setVelLimit(self.device.velocityLimit)
        self.setVoltageLimit(self.device.voltageLimit)

        self.device.addConnectionStateListener(self)
        self.device.commProvider.commandDataReceived.connect(self.commandResponseReceived)

        self.connectionStateChanged(self.device.isConnected)

    def connectionStateChanged(self, deviceConnected):
        if deviceConnected is True:
            self.enabeUI()
        else:
            self.disableUI()

    def enabeUI(self):
        self.setEnabled(True)

    def disableUI(self):
        self.setEnabled(False)

    def setLowPassFilter(self,value):
        self.lpfLineEdit.setText(str(value))

    def setPGain(self,value):
        self.pgainLineEdit.setText(str(value))

    def setVelLimit(self,value):
        self.vlLineEdit.setText(str(value))

    def setVoltageLimit(self,value):
        self.volLLineEdit.setText(str(value))

    def sendLowPassFilterAction(self):
        value = self.lpfLineEdit.text()
        value = value.replace(',', '.')
        self.lpfLineEdit.setText(value)
        self.device.sendLowPassFilter(self.lpfLineEdit.text())

    def sendPGainAction(self):
        value = self.pgainLineEdit.text()
        value = value.replace(',', '.')
        self.pgainLineEdit.setText(value)
        self.device.sendPGain(self.pgainLineEdit.text())

    def sendVelLimitAction(self):
        value = self.vlLineEdit.text()
        value = value.replace(',', '.')
        self.vlLineEdit.setText(value)
        self.device.sendVelocityLimit(self.vlLineEdit.text())

    def sendVoltageLimitAction(self):
        value = self.volLLineEdit.text()
        value = value.replace(',', '.')
        self.volLLineEdit.setText(value)
        self.device.sendVoltageLimit(self.volLLineEdit.text())

    def commandResponseReceived(self, comandResponse):
        if 'P angle|  P:' in comandResponse:
            self.pgainLineEdit.setText(
                comandResponse.replace('P angle|  P:', ''))
        elif 'Limits| vel_limit:' in comandResponse:
            self.vlLineEdit.setText(
                comandResponse.replace('Limits| vel_limit:', ''))
        elif 'Limits| volt_limit:' in comandResponse:
            self.volLLineEdit.setText(
                comandResponse.replace('Limits| volt_limit:', ''))
        elif 'LPF velocity| Tf:' in comandResponse:
            self.lpfLineEdit.setText(
                comandResponse.replace('LPF velocity| Tf:', ''))
