#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QTreeWidget

from src.gui.sharedcomnponets.sharedcomponets import GUIToolKit
from src.simpleFOCConnector import SimpleFOCDevice, PIDController, LowPassFilter


class DeviceTreeView(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.device = SimpleFOCDevice.getInstance()

        self.sFOCDevice = QtWidgets.QTreeWidgetItem(self)
        self.sFOCDevice.setText(0, 'sFOC Device')
        self.sFOCDevice.setIcon(0, GUIToolKit.getIconByName('motor'))


        self.motionControl = QtWidgets.QTreeWidgetItem(self.sFOCDevice)
        self.motionControl.setText(0, 'Motion config')
        self.motionControl.setIcon(0, GUIToolKit.getIconByName('pidconfig'))
        self.sFOCDevice.addChild(self.motionControl)

        self.controller = QtWidgets.QTreeWidgetItem(self.motionControl)
        self.controller.setText(0, 'Motion Control Type')
        self.controller.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.motionControl.addChild(self.controller)
        self.controllerValue = QtWidgets.QTreeWidgetItem(self.controller)
        self.controllerValue.setText(0, '')
        self.controllerValue.setFlags(
            self.controllerValue.flags() | QtCore.Qt.ItemIsEditable)
        self.controller.addChild(self.controllerValue)

        self.torque = QtWidgets.QTreeWidgetItem(self.motionControl)
        self.torque.setText(0, 'Torque Control Type')
        self.torque.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.motionControl.addChild(self.torque)
        self.torqueValue = QtWidgets.QTreeWidgetItem(self.torque)
        self.torqueValue.setText(0, '')
        self.torqueValue.setFlags(
            self.torqueValue.flags() | QtCore.Qt.ItemIsEditable)
        self.torque.addChild(self.torqueValue)
        
        self.motionDownsample = QtWidgets.QTreeWidgetItem(self.motionControl)
        self.motionDownsample.setText(0, 'Motion Downsample')
        self.motionDownsample.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.motionControl.addChild(self.motionDownsample)
        self.motionDownsampleValue = QtWidgets.QTreeWidgetItem(self.motionDownsample)
        self.motionDownsampleValue.setText(0, '')
        self.motionDownsampleValue.setFlags(
            self.motionDownsampleValue.flags() | QtCore.Qt.ItemIsEditable)
        self.motionDownsample.addChild(self.motionDownsampleValue)
        
        self.PIDVelocityConfig = self.addPIDSubtree(self.motionControl,'Velocity PID')
        self.PIDAngleConfig = self.addPIDSubtree(self.motionControl,'Angle PID')
        self.PIDCurrentQConfig = self.addPIDSubtree(self.motionControl,'Current q PID')
        self.PIDCurrentDConfig = self.addPIDSubtree(self.motionControl,'Current d PID')

        self.limitsConfig = QtWidgets.QTreeWidgetItem(self.sFOCDevice)
        self.limitsConfig.setText(0, 'Limits')
        self.limitsConfig.setIcon(0, GUIToolKit.getIconByName('statistics'))
        self.sFOCDevice.addChild(self.limitsConfig)

        self.velocityLimit = QtWidgets.QTreeWidgetItem(self.limitsConfig)
        self.velocityLimit.setText(0, 'Velocity limit')
        self.velocityLimit.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.limitsConfig.addChild(self.velocityLimit)
        self.velocityLimitValue = QtWidgets.QTreeWidgetItem(self.velocityLimit)
        self.velocityLimitValue.setText(0, '')
        self.velocityLimitValue.setFlags(
            self.velocityLimitValue.flags() | QtCore.Qt.ItemIsEditable)
        self.velocityLimit.addChild(self.velocityLimitValue)

        self.voltageLimit = QtWidgets.QTreeWidgetItem(self.limitsConfig)
        self.voltageLimit.setText(0, 'Voltage limit')
        self.voltageLimit.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.limitsConfig.addChild(self.voltageLimit)
        self.voltageLimitValue = QtWidgets.QTreeWidgetItem(self.voltageLimit)
        self.voltageLimitValue.setText(0, '')
        self.voltageLimitValue.setFlags(
            self.voltageLimitValue.flags() | QtCore.Qt.ItemIsEditable)
        self.voltageLimit.addChild(self.voltageLimitValue)

        self.currentLimit = QtWidgets.QTreeWidgetItem(self.limitsConfig)
        self.currentLimit.setText(0, 'Current limit')
        self.currentLimit.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.limitsConfig.addChild(self.currentLimit)
        self.currentLimitValue = QtWidgets.QTreeWidgetItem(self.currentLimit)
        self.currentLimitValue.setText(0, '')
        self.currentLimitValue.setFlags(
            self.currentLimitValue.flags() | QtCore.Qt.ItemIsEditable)
        self.currentLimit.addChild(self.currentLimitValue)


        self.statesConfig = QtWidgets.QTreeWidgetItem(self.sFOCDevice)
        self.statesConfig.setText(0, 'States')
        self.statesConfig.setIcon(0, GUIToolKit.getIconByName('statistics'))
        self.sFOCDevice.addChild(self.statesConfig)


        self.satateTarget = QtWidgets.QTreeWidgetItem(self.statesConfig)
        self.satateTarget.setText(0, 'Target')
        self.satateTarget.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.statesConfig.addChild(self.satateTarget)
        self.satateTargetValue = QtWidgets.QTreeWidgetItem(self.satateTarget)
        self.satateTargetValue.setText(0, '')
        self.satateTarget.addChild(self.satateTargetValue)

        self.stateVq = QtWidgets.QTreeWidgetItem(self.statesConfig)
        self.stateVq.setText(0, 'Voltage q')
        self.stateVq.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.statesConfig.addChild(self.stateVq)
        self.stateVqValue = QtWidgets.QTreeWidgetItem(self.stateVq)
        self.stateVq.addChild(self.stateVqValue)
        self.stateVd = QtWidgets.QTreeWidgetItem(self.statesConfig)
        self.stateVd.setText(0, 'Voltage d')
        self.stateVd.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.statesConfig.addChild(self.stateVd)
        self.stateVdValue = QtWidgets.QTreeWidgetItem(self.stateVd)
        self.stateVd.addChild(self.stateVdValue)

        self.stateCq = QtWidgets.QTreeWidgetItem(self.statesConfig)
        self.stateCq.setText(0, 'Current q')
        self.stateCq.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.statesConfig.addChild(self.stateCq)
        self.stateCqValue = QtWidgets.QTreeWidgetItem(self.stateCq)
        self.stateCq.addChild(self.stateVqValue)
        self.stateCd = QtWidgets.QTreeWidgetItem(self.statesConfig)
        self.stateCd.setText(0, 'Current d')
        self.stateCd.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.statesConfig.addChild(self.stateCd)
        self.stateCdValue = QtWidgets.QTreeWidgetItem(self.stateCd)
        self.stateCd.addChild(self.stateCdValue)

        self.stateVel = QtWidgets.QTreeWidgetItem(self.statesConfig)
        self.stateVel.setText(0, 'Velocity')
        self.stateVel.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.limitsConfig.addChild(self.stateVel)
        self.stateVelValue = QtWidgets.QTreeWidgetItem(self.stateVel)
        self.stateVelValue.setText(0, '')
        self.stateVel.addChild(self.stateVelValue)

        self.stateAngle = QtWidgets.QTreeWidgetItem(self.statesConfig)
        self.stateAngle.setText(0, 'Angle')
        self.stateAngle.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.limitsConfig.addChild(self.stateAngle)
        self.stateAngleValue = QtWidgets.QTreeWidgetItem(self.stateAngle)
        self.stateAngleValue.setText(0, '')
        self.stateAngle.addChild(self.stateAngleValue)


        self.sensorConfig = QtWidgets.QTreeWidgetItem(self.sFOCDevice)
        self.sensorConfig.setText(0, 'Sensor config')
        self.sensorConfig.setIcon(0, GUIToolKit.getIconByName('sensor'))
        self.sFOCDevice.addChild(self.sensorConfig)

        self.sensorZeroOffset = QtWidgets.QTreeWidgetItem(self.sensorConfig)
        self.sensorZeroOffset.setText(0, 'Zero Angle Offset')
        self.sensorZeroOffset.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.sensorConfig.addChild(self.sensorZeroOffset)
        self.sensorZeroOffsetValue = QtWidgets.QTreeWidgetItem(self.sensorZeroOffset)
        self.sensorZeroOffsetValue.setText(0, '')
        self.sensorZeroOffsetValue.setFlags(
            self.sensorZeroOffsetValue.flags() | QtCore.Qt.ItemIsEditable)
        self.sensorZeroOffset.addChild(self.sensorZeroOffsetValue)

        self.sensorZeroElecOffset = QtWidgets.QTreeWidgetItem(self.sensorConfig)
        self.sensorZeroElecOffset.setText(0, 'Electrical Zero Offset')
        self.sensorZeroElecOffset.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.sensorConfig.addChild(self.sensorZeroElecOffset)
        self.sensorZeroElecOffsetValue = QtWidgets.QTreeWidgetItem(self.sensorZeroElecOffset)
        self.sensorZeroElecOffsetValue.setText(0, '')
        self.sensorZeroElecOffsetValue.setFlags(
            self.sensorZeroElecOffsetValue.flags() | QtCore.Qt.ItemIsEditable)
        self.sensorZeroElecOffset.addChild(self.sensorZeroElecOffsetValue)

        self.generalSettings = QtWidgets.QTreeWidgetItem(self.sFOCDevice)
        self.generalSettings.setText(0, 'General settings')
        self.generalSettings.setIcon(0, GUIToolKit.getIconByName('generalsettings'))
        self.sFOCDevice.addChild(self.generalSettings)

        self.phaseRes = QtWidgets.QTreeWidgetItem(self.generalSettings)
        self.phaseRes.setText(0, 'Phase Resistance')
        self.phaseRes.setIcon(0, GUIToolKit.getIconByName('res'))
        self.generalSettings.addChild(self.phaseRes)
        self.phaseResValue = QtWidgets.QTreeWidgetItem(self.phaseRes)
        self.phaseResValue.setText(0, '')
        self.phaseResValue.setFlags(
            self.phaseResValue.flags() | QtCore.Qt.ItemIsEditable)
        self.phaseRes.addChild(self.phaseResValue)

        self.deviceStatus = QtWidgets.QTreeWidgetItem(self.generalSettings)
        self.deviceStatus.setText(0, 'Motor Status')
        self.deviceStatus.setIcon(0, GUIToolKit.getIconByName('gear'))
        self.generalSettings.addChild(self.deviceStatus)
        self.deviceStatusValue = QtWidgets.QTreeWidgetItem(self.deviceStatus)
        self.deviceStatusValue.setText(0, '')
        self.deviceStatusValue.setFlags(
            self.phaseResValue.flags() | QtCore.Qt.ItemIsEditable)
        self.deviceStatus.addChild(self.deviceStatusValue)


        self.setAlternatingRowColors(True)
        self.header().hide()
        self.expandItem(self.sFOCDevice)

        self.device.addConnectionStateListener(self)
        self.device.commProvider.commandDataReceived.connect(self.commandResponseReceived)

        self.itemChanged.connect(self.sendCommand)

        self.setEnabled(self.device.isConnected)

    def addPIDSubtree(self, parent,  label):
        pidConfiguration = QtWidgets.QTreeWidgetItem()
        pidConfiguration.setText(0, label)
        pidConfiguration.setIcon(0, GUIToolKit.getIconByName('pidconfig'))
        parent.addChild(pidConfiguration)

        proportionalGain = QtWidgets.QTreeWidgetItem(pidConfiguration)
        proportionalGain.setText(0, 'Proportional gain')
        proportionalGain.setIcon(0, GUIToolKit.getIconByName('gear'))
        proportionalValue = QtWidgets.QTreeWidgetItem(proportionalGain)
        proportionalValue.setText(0, '')
        proportionalValue.setFlags(
            proportionalValue.flags() | QtCore.Qt.ItemIsEditable)

        integralGain = QtWidgets.QTreeWidgetItem(pidConfiguration)
        integralGain.setText(0, 'Integral gain')
        integralGain.setIcon(0, GUIToolKit.getIconByName('gear'))
        integralGainValue = QtWidgets.QTreeWidgetItem(integralGain)
        integralGainValue.setText(0, '')
        integralGainValue.setFlags(
            integralGainValue.flags() | QtCore.Qt.ItemIsEditable)

        derivativeGain = QtWidgets.QTreeWidgetItem(pidConfiguration)
        derivativeGain.setText(0, 'Derivative gain')
        derivativeGain.setIcon(0, GUIToolKit.getIconByName('gear'))
        pidConfiguration.addChild(derivativeGain)
        derivativeGainValue = QtWidgets.QTreeWidgetItem(derivativeGain)
        derivativeGainValue.setText(0, '')
        derivativeGainValue.setFlags(
            derivativeGainValue.flags() | QtCore.Qt.ItemIsEditable)
        derivativeGain.addChild(derivativeGainValue)

        voltageRamp = QtWidgets.QTreeWidgetItem(pidConfiguration)
        voltageRamp.setText(0, 'Output Ramp')
        voltageRamp.setIcon(0, GUIToolKit.getIconByName('gear'))
        pidConfiguration.addChild(voltageRamp)
        voltageRampValue = QtWidgets.QTreeWidgetItem(voltageRamp)
        voltageRampValue.setText(0, '')
        voltageRampValue.setFlags(
            voltageRampValue.flags() | QtCore.Qt.ItemIsEditable)
        voltageRamp.addChild(voltageRampValue)
        
        limit = QtWidgets.QTreeWidgetItem(pidConfiguration)
        limit.setText(0, 'Output Limit')
        limit.setIcon(0, GUIToolKit.getIconByName('gear'))
        pidConfiguration.addChild(limit)
        limitValue = QtWidgets.QTreeWidgetItem(limit)
        limitValue.setText(0, '')
        limitValue.setFlags(
            limitValue.flags() | QtCore.Qt.ItemIsEditable)
        limit.addChild(limitValue)

        lpfTf = QtWidgets.QTreeWidgetItem(pidConfiguration)
        lpfTf.setText(0, 'Low pass filter')
        lpfTf.setIcon(0, GUIToolKit.getIconByName('gear'))
        pidConfiguration.addChild(lpfTf)
        lpfTfValue = QtWidgets.QTreeWidgetItem(lpfTf)
        lpfTfValue.setText(0, '')
        lpfTfValue.setFlags(
            lpfTfValue.flags() | QtCore.Qt.ItemIsEditable)
        lpfTf.addChild(lpfTfValue)
        return pidConfiguration



    def sendCommand(self, item, column):
        value = item.text(0)
        fieldName = item.parent().text(0)
        pidLabel = item.parent().parent().text(0)
        pid = {}
        lpf = {}
        if 'Velocity PID' in pidLabel:
            pid = self.device.PIDVelocity
            lpf = self.device.LPFVelocity
        elif 'Angle PID' in pidLabel:
            pid = self.device.PIDAngle
            lpf = self.device.LPFAngle
        elif 'Current q PID' in pidLabel:
            pid = self.device.PIDCurrentQ
            lpf = self.device.LPFCurrentQ
        elif 'Current d PID' in pidLabel:
            pid = self.device.PIDCurrentD
            lpf = self.device.LPFCurrentQ

        if 'Proportional gain' in fieldName:
            self.device.sendProportionalGain(pid, value)
        elif 'Integral gain' in fieldName:
            self.device.sendIntegralGain(pid, value)
        elif 'Derivative gain' in fieldName:
            self.device.sendDerivativeGain(pid, value)
        elif 'Output Ramp' in fieldName:
            self.device.sendOutputRamp(pid, value)
        elif 'Low pass filter' in fieldName:
            self.device.sendLowPassFilter(lpf, value)
        elif 'Output Limit' in fieldName:
            self.device.sendOutputLimit(pid,value)
        elif 'Voltage limit' in fieldName:
            self.device.sendVoltageLimit(value)
        elif 'Velocity limit' in fieldName:
            self.device.sendVelocityLimit(value)
        elif 'Current limit' in fieldName:
            self.device.sendCurrentLimit(value)
        elif 'Phase Resistance' in fieldName:
            self.device.sendPhaseResistance(value)
        elif 'Zero Angle Offset' in fieldName:
            self.device.sendSensorZeroOffset(value)
        elif 'Electrical Zero Offset' in fieldName:
            self.device.sendSensorZeroElectrical(value)
        elif 'Torque Control Type' in fieldName:
            self.device.sendTorqueType(value)
        elif 'Motion Control Type' in fieldName:
            self.device.sendControlType(value)
        elif 'Motion Downsample' in fieldName:
            self.device.sendMotionDownsample(value)
        elif 'Motor Status' in fieldName:
            self.device.sendDeviceStatus(value)

    def refreshPIDSubtree(self, pidDisp, pidVal, lpfVal):
        pidDisp.child(0).child(0).setText(0,str(pidVal.P))
        pidDisp.child(1).child(0).setText(0,str(pidVal.I))
        pidDisp.child(2).child(0).setText(0,str(pidVal.D))
        pidDisp.child(3).child(0).setText(0,str(pidVal.outputRamp))
        pidDisp.child(4).child(0).setText(0,str(pidVal.outputLimit))
        pidDisp.child(5).child(0).setText(0,str(lpfVal.Tf))

    def commandResponseReceived(self, comandResponse):
        self.refreshDeviceTree()


    def refreshDeviceTree(self):
        self.blockSignals(True)

        self.refreshPIDSubtree( self.PIDVelocityConfig, self.device.PIDVelocity, self.device.LPFVelocity)
        self.refreshPIDSubtree( self.PIDAngleConfig, self.device.PIDAngle, self.device.LPFAngle)
        self.refreshPIDSubtree( self.PIDCurrentQConfig, self.device.PIDCurrentQ, self.device.LPFCurrentQ)
        self.refreshPIDSubtree( self.PIDCurrentDConfig, self.device.PIDCurrentD, self.device.LPFCurrentD)

        self.voltageLimitValue.setText(0,str(self.device.voltageLimit))
        self.velocityLimitValue.setText(0,str(self.device.velocityLimit))
        self.currentLimitValue.setText(0,str(self.device.currentLimit))

        self.sensorZeroOffsetValue.setText(0,str(self.device.sensorZeroOffset))
        self.sensorZeroElecOffsetValue.setText(0,str(self.device.sensorElectricalZero))
        
        self.phaseResValue.setText(0,str(self.device.phaseResistance))
        self.deviceStatusValue.setText(0,str(self.device.deviceStatus))

        self.stateVelValue.setText(0,str(self.device.velocityNow))
        self.stateAngleValue.setText(0,str(self.device.angleNow))
        self.stateVdValue.setText(0,str(self.device.voltageDNow))
        self.stateVqValue.setText(0,str(self.device.voltageQNow))
        self.stateCqValue.setText(0,str(self.device.currentQNow))
        self.stateCdValue.setText(0,str(self.device.currentDNow))
        self.satateTargetValue.setText(0,str(self.device.targetNow))

        self.motionDownsampleValue.setText(0,str(self.device.motionDownsample))
        self.torqueValue.setText(0,str(self.device.torqueType))
        self.controllerValue.setText(0,str(self.device.controlType))
        self.update()
        self.blockSignals(False)

    def connectionStateChanged(self, connectionFlag):
        if connectionFlag is True:
            self.setEnabled(True)
        else:
            self.setEnabled(False)
