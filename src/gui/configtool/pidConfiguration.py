#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import (QtGui, QtWidgets, QtCore)
from src.gui.sharedcomnponets.sharedcomponets import ConfigQLineEdit
from src.simpleFOCConnector import SimpleFOCDevice


class PidGroupBox(QtWidgets.QGroupBox):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setMaximumWidth(300)

        onlyFloatInputValidator = QtGui.QRegExpValidator(
            QtCore.QRegExp("[+-]?([0-9]*[.])?[0-9]+"))

        self.device = SimpleFOCDevice.getInstance()

            
        self.activePID = self.device.PIDVelocity
        self.activeLPF = self.device.LPFVelocity

        self.setObjectName('pidConfigurator')
        self.setTitle('PID Controller configuration')

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName('gridLayout')
        
        self.sPidLabel = QtWidgets.QLabel(self)
        self.sPidLabel.setObjectName('pgLabel')
        self.sPidLabel.setText('Select PID')
        self.gridLayout.addWidget(self.sPidLabel, 0, 1, 1, 1)

        self.selectorPIDF = QtWidgets.QComboBox(self)
        self.selectorPIDF.setObjectName('selectPIDF')
        self.selectorPIDF.addItems(['Velocity', 'Angle', 'Current Q', 'Current D'])
        self.selectorPIDF.currentIndexChanged.connect(self.changePIDF)
        self.gridLayout.addWidget(self.selectorPIDF, 0, 2, 1, 1)

        self.pgLabel = QtWidgets.QLabel(self)
        self.pgLabel.setObjectName('pgLabel')
        self.pgLabel.setText('Proportional gain')
        self.gridLayout.addWidget(self.pgLabel, 1, 1, 1, 1)

        self.iglabel = QtWidgets.QLabel(self)
        self.iglabel.setObjectName('iglabel')
        self.iglabel.setText('Integral gain')
        self.gridLayout.addWidget(self.iglabel, 2, 1, 1, 1)

        self.dgLabel = QtWidgets.QLabel(self)
        self.dgLabel.setObjectName('dgLabel')
        self.dgLabel.setText('Derivative gain')
        self.gridLayout.addWidget(self.dgLabel, 3, 1, 1, 1)

        self.vrLabel = QtWidgets.QLabel(self)
        self.vrLabel.setObjectName('vrLabel')
        self.vrLabel.setText('Output ramp')
        self.gridLayout.addWidget(self.vrLabel, 4, 1, 1, 1)

        self.vrLabel = QtWidgets.QLabel(self)
        self.vrLabel.setObjectName('lpfLabel')
        self.vrLabel.setText('Low pass filter')
        self.gridLayout.addWidget(self.vrLabel, 5, 1, 1, 1)

        self.pgLineEdit = ConfigQLineEdit(self)
        self.pgLineEdit.setObjectName('pgLineEdit')
        self.pgLineEdit.setValidator(onlyFloatInputValidator)
        self.pgLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.pgLineEdit.editingFinished.connect(self.sendProportionalGainAction)
        self.gridLayout.addWidget(self.pgLineEdit, 1, 2, 1, 1)

        self.igLineEdit = ConfigQLineEdit(self)
        self.igLineEdit.setObjectName('igLineEdit')
        self.igLineEdit.setValidator(onlyFloatInputValidator)
        self.igLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.igLineEdit.editingFinished.connect(self.sendIntegralGainAction)
        self.gridLayout.addWidget(self.igLineEdit, 2, 2, 1, 1)

        self.dgLineEdit = ConfigQLineEdit(self)
        self.dgLineEdit.setObjectName('dgLineEdit')
        self.dgLineEdit.setValidator(onlyFloatInputValidator)
        self.dgLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dgLineEdit.editingFinished.connect(self.sendDerivativeGainAction)
        self.gridLayout.addWidget(self.dgLineEdit, 3, 2, 1, 1)
        
        self.vrLineEdit = ConfigQLineEdit(self)
        self.vrLineEdit.setObjectName('vrLineEdit')
        self.vrLineEdit.setValidator(onlyFloatInputValidator)
        self.vrLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.vrLineEdit.editingFinished.connect(self.sendRampAction)
        self.gridLayout.addWidget(self.vrLineEdit, 4, 2, 1, 1)

        self.lpfLineEdit = ConfigQLineEdit(self)
        self.lpfLineEdit.setObjectName('lpfLineEdit')
        self.lpfLineEdit.setValidator(onlyFloatInputValidator)
        self.lpfLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lpfLineEdit.editingFinished.connect(self.sendLPFAction)
        self.gridLayout.addWidget(self.lpfLineEdit, 5, 2, 1, 1)

        self.reloadPIDValues()

        # self.setDerivativeGainAction(self.device.derivativeGainPID)
        # self.setProportionalGainAction(self.device.proportionalGainPID)
        # self.setIntegralGainAction(self.device.integralGainPID)
        # self.setVoltageRampAction(self.device.voltageRampPID)

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

    def sendDerivativeGainAction(self):
        value = self.dgLineEdit.text()
        value = value.replace(',', '.')
        self.dgLineEdit.setText(value)
        self.device.sendDerivativeGain(self.activePID, value)

    def sendProportionalGainAction(self):
        value = self.pgLineEdit.text()
        value = value.replace(',', '.')
        self.pgLineEdit.setText(value)
        self.device.sendProportionalGain(self.activePID, self.pgLineEdit.text())

    def sendIntegralGainAction(self):
        value = self.igLineEdit.text()
        value = value.replace(',', '.')
        self.igLineEdit.setText(value)
        self.device.sendIntegralGain(self.activePID, self.igLineEdit.text())

    def sendRampAction(self):
        value = self.vrLineEdit.text()
        value = value.replace(',', '.')
        self.vrLineEdit.setText(value)
        self.device.sendOutputRamp(self.activePID, self.vrLineEdit.text())

    def sendLPFAction(self):
        value = self.lpfLineEdit.text()
        value = value.replace(',', '.')
        self.lpfLineEdit.setText(value)
        self.device.sendLowPassFilter(self.activeLPF, self.lpfLineEdit.text())

    def reloadPIDValues(self):
        self.pgLineEdit.setText(str(self.activePID.P))
        self.dgLineEdit.setText(str(self.activePID.D))
        self.igLineEdit.setText(str(self.activePID.I))
        self.vrLineEdit.setText(str(self.activePID.outputRamp))
        self.lpfLineEdit.setText(str(self.activeLPF.Tf))

    def changePIDF(self):
        index = self.selectorPIDF.currentIndex()
        if index == 0:
            self.activePID = self.device.PIDVelocity
            self.activeLPF = self.device.LPFVelocity
        elif index == 1:
            self.activePID = self.device.PIDAngle
            self.activeLPF = self.device.LPFAngle
        elif index == 2:
            self.activePID = self.device.PIDCurrentQ
            self.activeLPF = self.device.LPFCurrentQ
        elif index == 3:
            self.activePID = self.device.PIDCurrentD
            self.activeLPF = self.device.LPFCurrentD

        self.device.pullPIDConf(self.activePID, self.activeLPF)
        self.reloadPIDValues()

    def commandResponseReceived(self, commandDataReceived):
        self.pgLineEdit.setText(str(self.activePID.P))
        self.dgLineEdit.setText(str(self.activePID.D))
        self.igLineEdit.setText(str(self.activePID.I))
        self.vrLineEdit.setText(str(self.activePID.outputRamp))
        self.lpfLineEdit.setText(str(self.activeLPF.Tf))

