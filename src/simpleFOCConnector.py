#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import threading
import time
import serial
from PyQt5 import QtCore, QtWidgets
from serial import SerialException


class SimpleFOCDevice:
    __instance = None

    VOLTAGE_CONTROL = 0
    VELOCITY_CONTROL = 1
    ANGLE_CONTROL = 2

    PULL_CONFIG_ON_CONNECT = 'Pull config'
    PUSH_CONFG_ON_CONNECT = 'Push config'
    ONLY_CONNECT = 'Only connect'

    @staticmethod
    def getInstance():
        """ Static access method. """
        if SimpleFOCDevice.__instance == None:
            SimpleFOCDevice()
        return SimpleFOCDevice.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SimpleFOCDevice.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.serialPort = None
            self.responseThread = None
            self.isConnected = False
            self.openedFile = None

            self.connectionStateListenerList = []

            self.proportionalGainPID = 0
            self.integralGainPID = 0
            self.derivativeGainPID = 0
            self.voltageRampPID = 0
            self.lowPassFilter = 0
            self.anglePGain = 0
            self.velocityLimit = 0
            self.voltageLimit = 0
            self.controlType =  SimpleFOCDevice.ANGLE_CONTROL
            self.initialTarget = 0
            self.connectionID = ""
            self.serialPortName = ""
            self.serialRate = 115200
            self.serialByteSize = serial.EIGHTBITS
            self.serialParity = serial.PARITY_NONE
            self.stopBits = serial.STOPBITS_ONE
            self.target = 0
            self.commProvider = SerialPortReceiveHandler()
            SimpleFOCDevice.__instance = self

    def configueDevice(self, jsonValue):
        self.proportionalGainPID = jsonValue['proportionalGainPID']
        self.integralGainPID = jsonValue['integralGainPID']
        self.derivativeGainPID = jsonValue['derivativeGainPID']
        self.voltageRampPID = jsonValue['voltageRampPID']
        self.lowPassFilter = jsonValue['lowPassFilter']
        self.anglePGain = jsonValue['anglePGain']
        self.velocityLimit = jsonValue['velocityLimit']
        self.voltageLimit = jsonValue['voltageLimit']
        self.controlType = jsonValue['controlType']
        self.initialTarget = jsonValue['initialTarget']
        self.connectionID = jsonValue['connectionID']
        self.serialPortName = jsonValue['serialPortName']
        self.serialRate = jsonValue['serialRate']
        self.serialByteSize = jsonValue['serialByteSize']
        self.serialParity = jsonValue['serialParity']
        self.stopBits = jsonValue['stopBits']

    def configureConnection(self, configDict):

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
            return 'Angle', 'Voltage Q', 'Angle SP'

    @staticmethod
    def getControlModeCode(mode):
        if mode == 'angle':
            return SimpleFOCDevice.ANGLE_CONTROL
        elif mode == 'voltage':
            return SimpleFOCDevice.VOLTAGE_CONTROL
        elif mode == 'velocity':
            return SimpleFOCDevice.VELOCITY_CONTROL

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

    def connect(self, connectionMode):
        try:
            self.__initCommunications()
        except SerialException as serEx:
            logging.warning('Is not possible to open serial port')
            logging.warning('Port =' + self.serialPortName)
            logging.warning('Rate =' + str(self.serialRate))
            logging.warning('parity =' + str(self.serialParity))
            logging.warning('Byte size =' + str(self.serialByteSize))
            logging.warning('Stop bits=' + str(self.stopBits))

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
                listener.connectionStateChanged(True)
            if connectionMode == SimpleFOCDevice.PULL_CONFIG_ON_CONNECT:
                self.pullConfiguration()
            elif connectionMode == SimpleFOCDevice.PUSH_CONFG_ON_CONNECT:
                self.pushConfiguration()
                pass
            return True

    def disConnect(self):
        self.isConnected = False
        self.__closeCommunication()
        for listener in self.connectionStateListenerList:
            listener.connectionStateChanged(False)

    def addConnectionStateListener(self, listener):
        self.connectionStateListenerList.append(listener)

    def sendCommand(self, command):
        if self.isConnected:
            self.serialPort.write((str(command) + '\n').encode('utf-8'))

    def sendControlType(self, loop_control_type):
        if self.isConnected:
            self.sendCommand('C' + str(loop_control_type))

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
            # TODO TODO TODO
            raise NotImplemented

    def sendHaltDevice(self):
        if self.isConnected:
            # TODO TODO TODO
            raise NotImplemented

    def pushConfiguration(self):
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

    def pullConfiguration(self):
            self.sendControlType('')
            time.sleep(5 / 1000)
            self.sendProportionalGain('')
            time.sleep(5 / 1000)
            self.sendIntegralGain('')
            time.sleep(5 / 1000)
            self.sendDerivativeGain('')
            time.sleep(5 / 1000)
            self.sendVoltageRamp('')
            time.sleep(5 / 1000)
            self.sendLowPassFilter('')
            time.sleep(5 / 1000)
            self.sendPGain('')
            time.sleep(5 / 1000)
            self.sendVelocityLimit('')
            time.sleep(5 / 1000)
            self.sendVoltageLimit('')

class SerialPortReceiveHandler(QtCore.QThread):
    telemetryDataReceived = QtCore.pyqtSignal(float, float, float)
    commandDataReceived = QtCore.pyqtSignal(str)
    rawDataReceived = QtCore.pyqtSignal(str)

    def __init__(self, serial_port=None, *args,**kwargs):
        super(SerialPortReceiveHandler, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.serialComm = serial_port

    def handle_received_data(self, data):
        if self.isDataReceivedTelementry(data):
            try:
                v = data.rstrip().split('\t', 3)
                self.telemetryDataReceived.emit(float(v[2]), float(v[1]),
                                                float(v[0]))
            except ValueError as error:
                logging.error(error, exc_info=True)
                logging.error('data =' + str(data), exc_info=True)
            except IndexError as error:
                logging.error(error, exc_info=True)
                logging.error('data =' + str(data), exc_info=True)
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
