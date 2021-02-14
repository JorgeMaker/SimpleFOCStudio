#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
from serial import SerialException
import threading
from PyQt5 import QtCore, QtWidgets
import logging

class SimpleFOCDevice():

    VOLTAGE_CONTROL = 0
    VELOCITY_CONTROL = 1
    ANGLE_CONTROL = 2

    def __init__(self, pid_p=0, pid_i=0, pid_d=0, v_ramp=0, lpf=0,
                 a_gain=0, vel_lim=0, v_limit=0, ctr_type=ANGLE_CONTROL,
                 initial_target=0,conn_id='',port='',byte_size=serial.EIGHTBITS,
                 parity=serial.PARITY_NONE, stop_bits=serial.STOPBITS_ONE):

        self.serialPort = None
        self.responseThread = None
        self.isConnected = False
        self.openedFile = None

        self.connectionStateListenerList = []
        self.controlLoopModeListenerList = []

        self.proportionalGainPID = pid_p
        self.integralGainPID = pid_i
        self.derivativeGainPID = pid_d
        self.voltageRampPID = v_ramp
        self.lowPassFilter = lpf
        self.anglePGain = a_gain
        self.velocityLimit = vel_lim
        self.voltageLimit = v_limit
        self.controlType = ctr_type
        self.initialTarget = initial_target
        self.connectionID = conn_id
        self.serialPortName = port
        self.serialRate = 115200
        self.serialByteSize = byte_size
        self.serialParity = parity
        self.stopBits = stop_bits

        self.target = initial_target

        self.commProvider = SerialPortReceiveHandler()

    @staticmethod
    def fromJSON(jsonValue):

        device = SimpleFOCDevice()

        device.proportionalGainPID = jsonValue['proportionalGainPID']
        device.integralGainPID = jsonValue['integralGainPID']
        device.derivativeGainPID = jsonValue['derivativeGainPID']
        device.voltageRampPID = jsonValue['voltageRampPID']
        device.lowPassFilter = jsonValue['lowPassFilter']
        device.anglePGain = jsonValue['anglePGain']
        device.velocityLimit = jsonValue['velocityLimit']
        device.voltageLimit = jsonValue['voltageLimit']
        device.controlType = jsonValue['controlType']
        device.initialTarget = jsonValue['initialTarget']
        device.connectionID = jsonValue['connectionID']
        device.serialPortName = jsonValue['serialPortName']
        device.serialRate = jsonValue['serialRate']
        device.serialByteSize = jsonValue['serialByteSize']
        device.serialParity = jsonValue['serialParity']
        device.stopBits = jsonValue['stopBits']

        return device

    def configureDevice(self, configDict):

        self.connectionID = configDict['connectionID']
        self.serialPortName = configDict['serialPortName']
        self.serialRate = configDict['serialRate']
        self.serialByteSize = configDict['serialByteSize']
        self.serialParity = configDict['serialParity']
        self.stopBits = configDict['stopBits']

    def toJSON(self):

        valuesToSave = {
            'proportionalGainPID': self.proportionalGainPID,
            'integralGainPID': self.integralGainPID,
            'derivativeGainPID': self.derivativeGainPID,
            'voltageRampPID': self.voltageRampPID,
            'lowPassFilter': self.lowPassFilter,
            'anglePGain': self.anglePGain,
            'velocityLimit': self.velocityLimit,
            'voltageLimit': self.voltageLimit,
            'controlType': self.controlType,
            'initialTarget': self.initialTarget,
            'connectionID': self.connectionID,
            'serialPortName': self.serialPortName,
            'serialRate': self.serialRate,
            'serialByteSize': self.serialByteSize,
            'serialParity': self.serialParity,
            'stopBits': self.stopBits
        }
        return valuesToSave

    @staticmethod
    def getSignalLabels(controlMode):
        if controlMode is SimpleFOCDevice.VOLTAGE_CONTROL:
            return 'Velocity', 'Voltage Q', 'Angle'
        # return 'Voltage Q','Angle','Velocity'  ¿Correct?
        if controlMode is SimpleFOCDevice.VELOCITY_CONTROL:
        # return 'Voltage Q','Velocity SP','Velocity' ¿Correct?
            return 'Velocity', 'Voltage Q', 'Velocity SP'
        if controlMode is SimpleFOCDevice.ANGLE_CONTROL:
        #   return 'Voltage Q','Angle SP','Angle' ¿Correct?
            return 'Angle','Voltage Q','Angle SP'

    def __initCommunications(self):
        self.serialPort = serial.Serial(self.serialPortName,
                                        self.serialRate,
                                        self.serialByteSize,
                                        self.serialParity,
                                        self.stopBits)

        self.commProvider.serialComm = self.serialPort
        self.commProvider.start()

    def __closeCommunication(self):
        self.serialPort.close()

    def connect(self):
        try:
            self.__initCommunications()
        except SerialException as serEx:
            logging.warning('Is not possible to open serial port')
            logging.warning('Port ='+self.serialPortName)
            logging.warning('Rate ='+str(self.serialRate))
            logging.warning('parity ='+str(self.serialParity))
            logging.warning('Byte size ='+str(self.serialByteSize))
            logging.warning('Stop bits='+str(self.stopBits))

            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText('Error while trying to open serial port')
            msgBox.setWindowTitle('SimpleFOC ConfigTool')
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
            return False
        else:
            self.isConnected = True
            for listener in self.connectionStateListenerList:
                listener.deviceConnected(True)
            self.sendFullConfiguration()
            return True

    def disConnect(self):
        #self.commProvider.stop()
        self.isConnected = False
        self.__closeCommunication()
        for listener in self.connectionStateListenerList:
            listener.deviceConnected(False)

    def addConnectionStateListener(self, listener):
        self.connectionStateListenerList.append(listener)

    def addControlLoopModeListener(self, listener):
        self.controlLoopModeListenerList.append(listener)

    def sendCommand(self, command):
        if self.isConnected:
            self.serialPort.write((str(command) +'\n').encode('utf-8'))

    def sendControlType(self, loop_control_type):
        if self.isConnected:
            self.sendCommand('C' + str(loop_control_type))
            for listener in self.controlLoopModeListenerList:
                listener.controlLoopModeChanged(loop_control_type)

    def sendProportionalGain(self, value):
        if self.isConnected:
            self.proportionalGainPID = value
            self.sendCommand('P' + str(value))

    def sendIntegralGain(self, value):
        if self.isConnected:
            self.integralGainPID = value
            self.sendCommand('I' + str(value))

    def sendDerivativeGain(self, value):
        if self.isConnected:
            self.derivativeGainPID = value
            self.sendCommand('D' + str(value))

    def sendVoltageRamp(self, value):
        if self.isConnected:
            self.voltageRampPID = value
            self.sendCommand('R' + str(value))

    def sendLowPassFilter(self, value):
        if self.isConnected:
            self.lowPassFilter = value
            self.sendCommand('F' + str(value))

    def sendPGain(self, value):
        if self.isConnected:
            self.anglePGain = value
            self.sendCommand('K' + str(value))

    def sendVelocityLimit(self, value):
        if self.isConnected:
            self.velocityLimit = value
            self.sendCommand('N' + str(value))

    def sendVoltageLimit(self, value):
        if self.isConnected:
            self.voltageLimit = value
            self.sendCommand('L' + str(value))

    def sendTargetValue(self, targetvalue):
        if self.isConnected:
            self.target = targetvalue
            self.sendCommand(self.target)

    def sendZeroEncoder(self):
        if self.isConnected:
            raise NotImplemented
            #  TODO

    def sendHaltDevice(self):
        if self.isConnected:
            raise NotImplemented
            #  TODO

    def sendFullConfiguration(self):
        self.sendControlType(self.controlType)
        self.sendProportionalGain(self.proportionalGainPID)
        self.sendIntegralGain(self.integralGainPID)
        self.sendDerivativeGain(self.derivativeGainPID)
        self.sendVoltageRamp(self.voltageRampPID)
        self.sendLowPassFilter(self.lowPassFilter)
        self.sendPGain(self.anglePGain)
        self.sendVelocityLimit(self.velocityLimit)
        self.sendVoltageLimit(self.voltageLimit)
        self.sendTargetValue(self.initialTarget)

class SerialPortReceiveHandler(QtCore.QThread):

    telemetryDataReceived = QtCore.pyqtSignal(float, float, float)
    commandDataReceived = QtCore.pyqtSignal(str)
    rawDataReceived = QtCore.pyqtSignal(str)

    def __init__(self, serial_port=None, *args, **kwargs):
        super(SerialPortReceiveHandler, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

        self.serialComm = serial_port

    def handle_received_data(self, data):
        if self.isDataReceivedTelementry(data):
            try:
                v = data.rstrip().split('\t', 3)
                self.telemetryDataReceived.emit(float(v[2]), float(v[1]), float(v[0]))
            except ValueError as error:
                logging.error(error, exc_info=True)
                logging.error('data ='+str(data), exc_info=True)
            except IndexError as error:
                logging.error(error, exc_info=True)
                logging.error('data ='+str(data), exc_info=True)
        else:
            self.commandDataReceived.emit(data.rstrip())
        self.rawDataReceived.emit(data.rstrip())

    def isDataReceivedTelementry(self, data):
        if data[0].isdigit() or data[0] == '-':
            return True
        else:
            return False

    def run(self):
        try:
            while not self.stopped():
                if self.serialComm is not None:
                    if self.serialComm.isOpen():
                        reading = self.serialComm.readline().decode()
                        self.handle_received_data(reading)
        except SerialException as serialException:
            logging.error(serialException, exc_info=True)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
