#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import (QtGui, QtWidgets, QtCore)

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

        self.motionDownsample = QtWidgets.QLabel(self)
        self.motionDownsample.setObjectName('motionDownsample')
        self.motionDownsample.setText('Motion Downsample')
        self.gcGridLayout.addWidget(self.motionDownsample, 2, 0, 1, 1)

        self.motionDownsampleEdit = ConfigQLineEdit(self)
        self.motionDownsampleEdit.setObjectName('motionDownsampleEdit')
        self.motionDownsampleEdit.setValidator(onlyFloat)
        self.motionDownsampleEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.motionDownsampleEdit.updateValue.connect(self.sendMotionDownsampleAction)
        self.gcGridLayout.addWidget(self.motionDownsampleEdit, 2, 1, 1, 1)

        self.curLimitLabel = QtWidgets.QLabel(self)
        self.curLimitLabel.setObjectName('curLimitLabel')
        self.curLimitLabel.setText('Current Limit')
        self.gcGridLayout.addWidget(self.curLimitLabel, 3, 0, 1, 1)

        self.velLimitlabel = QtWidgets.QLabel(self)
        self.velLimitlabel.setObjectName('velLimitlabel')
        self.velLimitlabel.setText('Velocity limit')
        self.gcGridLayout.addWidget(self.velLimitlabel, 4, 0, 1, 1)

        self.volLimitLabel = QtWidgets.QLabel(self)
        self.volLimitLabel.setObjectName('volLimitLabel')
        self.volLimitLabel.setText('Voltage limit')
        self.gcGridLayout.addWidget(self.volLimitLabel, 6, 0, 1, 1)

        self.clLineEdit = ConfigQLineEdit(self)
        self.clLineEdit.setObjectName('clLineEdit')
        self.clLineEdit.setValidator(onlyFloat)
        self.clLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.clLineEdit.updateValue.connect(self.sendCurrentLimitAction)
        self.gcGridLayout.addWidget(self.clLineEdit, 3, 1, 1, 1)

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

        self.reloadValues()

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

    def sendMotionDownsampleAction(self):
        value = self.motionDownsampleEdit.text()
        value = value.replace(',', '.')
        self.motionDownsampleEdit.setText(value)
        self.device.sendMotionDownsample(value)

    def sendCurrentLimitAction(self):
        value = self.clLineEdit.text()
        value = value.replace(',', '.')
        self.clLineEdit.setText(value)
        self.device.sendCurrentLimit(self.clLineEdit.text())

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
        self.reloadValues()
        
    def reloadValues(self):
        self.motionDownsampleEdit.setText(str(self.device.motionDownsample))
        self.clLineEdit.setText(str(self.device.currentLimit))
        self.vlLineEdit.setText(str(self.device.velocityLimit))
        self.volLLineEdit.setText(str(self.device.voltageLimit))