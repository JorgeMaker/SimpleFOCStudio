#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QTreeWidget

from src.gui.sharedcomnponets.sharedcomponets import GUIToolKit
from src.simpleFOCConnector import SimpleFOCDevice


class DeviceTreeView(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.device = SimpleFOCDevice.getInstance()

        self.sFOCDevice = QtWidgets.QTreeWidgetItem(self)
        self.sFOCDevice.setText(0, 'sFOC Device')
        self.sFOCDevice.setIcon(0, GUIToolKit.getIconByName('motor'))

        self.pidConfiguration = QtWidgets.QTreeWidgetItem(self.sFOCDevice)
        self.pidConfiguration.setText(0, 'Pid configuration')
        self.pidConfiguration.setIcon(0, GUIToolKit.getIconByName('pidconfig'))
        self.sFOCDevice.addChild(self.pidConfiguration)

        self.proportionalGain = QtWidgets.QTreeWidgetItem(self.pidConfiguration)
        self.proportionalGain.setText(0, 'Proportional gain')
        self.proportionalGain.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.pidConfiguration.addChild(self.proportionalGain)
        self.proportionalValue = QtWidgets.QTreeWidgetItem(self.proportionalGain)
        self.proportionalValue.setText(0, '')
        self.proportionalValue.setFlags(
            self.proportionalValue.flags() | QtCore.Qt.ItemIsEditable)
        self.proportionalGain.addChild(self.proportionalValue)

        self.integralGain = QtWidgets.QTreeWidgetItem(self.pidConfiguration)
        self.integralGain.setText(0, 'Integral gain')
        self.integralGain.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.pidConfiguration.addChild(self.integralGain)
        self.integralGainlValue = QtWidgets.QTreeWidgetItem(self.integralGain)
        self.integralGainlValue.setText(0, '')
        self.integralGainlValue.setFlags(
            self.integralGainlValue.flags() | QtCore.Qt.ItemIsEditable)
        self.integralGain.addChild(self.integralGainlValue)

        self.derivativeGain = QtWidgets.QTreeWidgetItem(self.pidConfiguration)
        self.derivativeGain.setText(0, 'Derivative gain')
        self.derivativeGain.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.pidConfiguration.addChild(self.derivativeGain)
        self.derivativeGainValue = QtWidgets.QTreeWidgetItem(self.derivativeGain)
        self.derivativeGainValue.setText(0, '')
        self.derivativeGainValue.setFlags(
            self.derivativeGainValue.flags() | QtCore.Qt.ItemIsEditable)
        self.derivativeGain.addChild(self.derivativeGainValue)

        self.voltageRamp = QtWidgets.QTreeWidgetItem(self.pidConfiguration)
        self.voltageRamp.setText(0, 'Voltage Ramp')
        self.voltageRamp.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.pidConfiguration.addChild(self.voltageRamp)
        self.voltageRampValue = QtWidgets.QTreeWidgetItem(self.voltageRamp)
        self.voltageRampValue.setText(0, '')
        self.voltageRampValue.setFlags(
            self.voltageRampValue.flags() | QtCore.Qt.ItemIsEditable)
        self.voltageRamp.addChild(self.derivativeGainValue)

        self.generalStttings = QtWidgets.QTreeWidgetItem(self.sFOCDevice)
        self.generalStttings.setText(0, 'General settings')
        self.generalStttings.setIcon(0, GUIToolKit.getIconByName('generalsettings'))
        self.sFOCDevice.addChild(self.generalStttings)

        self.lwpFilter = QtWidgets.QTreeWidgetItem(self.generalStttings)
        self.lwpFilter.setText(0, 'Low pass filterRamp')
        self.lwpFilter.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.generalStttings.addChild(self.lwpFilter)
        self.lwpFilterValue = QtWidgets.QTreeWidgetItem(self.lwpFilter)
        self.lwpFilterValue.setText(0, '')
        self.lwpFilterValue.setFlags(
            self.lwpFilterValue.flags() | QtCore.Qt.ItemIsEditable)
        self.lwpFilter.addChild(self.lwpFilterValue)

        self.pGain = QtWidgets.QTreeWidgetItem(self.generalStttings)
        self.pGain.setText(0, 'Prop gain')
        self.pGain.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.generalStttings.addChild(self.pGain)
        self.pGainValue = QtWidgets.QTreeWidgetItem(self.pGain)
        self.pGainValue.setText(0, '')
        self.pGainValue.setFlags(self.pGainValue.flags() | QtCore.Qt.ItemIsEditable)
        self.pGain.addChild(self.pGainValue)

        self.veliLimit = QtWidgets.QTreeWidgetItem(self.generalStttings)
        self.veliLimit.setText(0, 'Velocity limit')
        self.veliLimit.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.generalStttings.addChild(self.veliLimit)
        self.veliLimitValue = QtWidgets.QTreeWidgetItem(self.veliLimit)
        self.veliLimitValue.setText(0, '')
        self.veliLimitValue.setFlags(
            self.veliLimitValue.flags() | QtCore.Qt.ItemIsEditable)
        self.veliLimit.addChild(self.veliLimitValue)

        self.voliLimit = QtWidgets.QTreeWidgetItem(self.generalStttings)
        self.voliLimit.setText(0, 'Voltage limit')
        self.voliLimit.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.generalStttings.addChild(self.voliLimit)
        self.voliLimitValue = QtWidgets.QTreeWidgetItem(self.voliLimit)
        self.voliLimitValue.setText(0, '')
        self.voliLimitValue.setFlags(
            self.voliLimitValue.flags() | QtCore.Qt.ItemIsEditable)
        self.voliLimit.addChild(self.voliLimitValue)

        self.setAlternatingRowColors(True)
        self.header().hide()
        self.expandAll()

        self.device.addConnectionStateListener(self)
        self.device.commProvider.commandDataReceived.connect(self.commandResponseReceived)

        self.itemChanged.connect(self.sendCommand)


        self.proportionalValue.setText(0,str(self.device.proportionalGainPID))
        self.integralGainlValue.setText(0,str(self.device.integralGainPID))
        self.derivativeGainValue.setText(0,str(self.device.derivativeGainPID))
        self.voltageRampValue.setText(0,str(self.device.voltageRampPID))

        self.lwpFilterValue.setText(0,str(self.device.lowPassFilter))
        self.pGainValue.setText(0,str(self.device.anglePGain))
        self.veliLimitValue.setText(0,str(self.device.velocityLimit))
        self.voliLimitValue.setText(0,str(self.device.voltageLimit))

        self.setEnabled(False)

    def sendCommand(self, item, column):
        value = item.text(0)
        fieldName = item.parent().text(0)
        if 'Proportional gain' in fieldName:
            self.device.sendProportionalGain(value)
        elif 'Integral gain' in fieldName:
            self.device.sendIntegralGain(value)
        elif 'Derivative gain' in fieldName:
            self.device.sendDerivativeGain(value)
        elif 'Voltage Ramp' in fieldName:
            self.device.sendVoltageRamp(value)
        elif 'Low pass filterRamp' in fieldName:
            self.device.sendLowPassFilter(value)
        elif 'Prop gain' in fieldName:
            self.device.sendPGain(value)
        elif 'Velocity limit' in fieldName:
            self.device.sendVelocityLimit(value)
        elif 'Voltage limit' in fieldName:
            self.device.sendVoltageLimit(value)

    def commandResponseReceived(self, comandResponse):
        if 'PID velocity| P' in comandResponse:
            self.proportionalValue.setText(0,comandResponse.replace('PID velocity| P:', ''))
        elif 'PID velocity| I' in comandResponse:
            self.integralGainlValue.setText(0,comandResponse.replace('PID velocity| I:', ''))
        elif 'PID velocity| D' in comandResponse:
            self.derivativeGainValue.setText(0,comandResponse.replace('PID velocity| D:', ''))
        elif 'PID velocity| volt_ramp' in comandResponse:
            self.voltageRampValue.setText(0,comandResponse.replace('PID velocity| volt_ramp:', ''))
        elif 'LPF velocity| Tf:' in comandResponse:
            self.lwpFilterValue.setText(0,
                comandResponse.replace('LPF velocity| Tf:', ''))
        elif 'P angle|  P:' in comandResponse:
            self.pGainValue.setText(0,
                comandResponse.replace('P angle|  P:', ''))
        elif 'Limits| vel_limit:' in comandResponse:
            self.veliLimitValue.setText(0,
                comandResponse.replace('Limits| vel_limit:', ''))
        elif 'Limits| volt_limit:' in comandResponse:
            self.voliLimitValue.setText(0,
                comandResponse.replace('Limits| volt_limit:', ''))
        self.update()

    def connectionStateChanged(self, connectionFlag):
        if connectionFlag is True:
            self.setEnabled(True)
        else:
            self.setEnabled(False)
