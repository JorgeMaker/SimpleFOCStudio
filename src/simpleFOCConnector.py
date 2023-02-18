#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import threading
import time

import serial
from PyQt5 import QtCore, QtWidgets
from serial import SerialException
from collections import defaultdict

class PIDController:
    P = 0
    D = 0
    I = 0
    outputRamp = 0
    outputLimit = 0
    cmd =''

    def __init__(self, cmd):
        self.cmd = cmd
    
    def load(self, jsonValues):
        self.P = jsonValues['P']
        self.I = jsonValues['I']
        self.D = jsonValues['D']
        self.outputRamp = jsonValues['outputRamp']
        self.outputLimit = jsonValues['outputLimit']

    def serialize(self):
        return {
            'P': self.P,
            'I': self.I,
            'D': self.D,
            'outputRamp':self.outputRamp,
            'outputLimit':self.outputLimit
        }


class LowPassFilter:
    Tf = 0
    cmd =''
    cmdTf = 'F'

    def __init__(self, cmd):
        self.cmd = cmd


class Command:
    cmdName = ''
    cmd = ''

    def __init__(self,cmdname='Command', cmd=''):
        self.cmdName = cmdname
        self.cmd = cmd

    def load(self, jsonValues):
        self.cmdName = jsonValues['commandName']
        self.cmd = jsonValues['commandValue']

    def serialize(self):
        return {
            'commandName': self.cmdName,
            'commandValue': self.cmd
        }


class CustomCommands:
    customCommandsList = []

    def __init__(self,commandsLis=[]):
        for command in  commandsLis:
            self.customCommandsList.append(command)
    def load(self, jsonValues):
        for commandInJson in jsonValues:
            command = Command()
            command.load(commandInJson)
            self.customCommandsList.append(command)

    def serialize(self):
        serializedCustomCommands = defaultdict(list)
        for command in self.customCommandsList:
            serializedCommand = command.serialize()
            serializedCustomCommands['customCommands'].append(serializedCommand)
        return serializedCustomCommands

class SimpleFOCDevice:
    __instance = None

    TORQUE_CONTROL  = 0
    VELOCITY_CONTROL = 1
    ANGLE_CONTROL = 2
    VELOCITY_OPENLOOP_CONTROL = 3
    ANGLE_OPENLOOP_CONTROL = 4

    SINE_PWM  = 0
    SPACE_VECTOR_PWM = 1
    TRAPEZOIDAL_120 = 2
    TRAPEZOIDAL_150 = 3

    VOLTAGE_TORQUE = 0
    DC_CURRENT_TORQUE  = 1
    FOC_CURRENT_TORQUE = 2

    VELOCITY_PID = 'V'
    ANGLE_PID = 'A'
    CURRENT_Q_PID = 'Q'
    CURRENT_D_PID = 'D'

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
            # serial connection variables
            self.serialPort = None
            self.responseThread = None
            self.isConnected = False
            self.openedFile = None

            self.connectionStateListenerList = []

            self.serialPortName = ""
            self.serialRate = 115200
            self.serialByteSize = serial.EIGHTBITS
            self.serialParity = serial.PARITY_NONE
            self.stopBits = serial.STOPBITS_ONE
            self.commProvider = SerialPortReceiveHandler()
            self.commProvider.commandDataReceived.connect(self.parseResponses)
            self.commProvider.stateMonitorReceived.connect(self.parseStateResponses)
            self.connectionID = ""

            # command id of the device
            self.devCommandID = ''

            # motion control paramters
            self.PIDVelocity = PIDController(self.VELOCITY_PID)
            self.PIDAngle = PIDController(self.ANGLE_PID)
            self.PIDCurrentQ = PIDController(self.CURRENT_Q_PID)
            self.PIDCurrentD = PIDController(self.CURRENT_D_PID)
            self.LPFVelocity = LowPassFilter(self.VELOCITY_PID)
            self.LPFAngle = LowPassFilter(self.ANGLE_PID)
            self.LPFCurrentQ = LowPassFilter(self.CURRENT_Q_PID)
            self.LPFCurrentD = LowPassFilter(self.CURRENT_D_PID)
            self.velocityLimit = 0
            self.voltageLimit = 0
            self.currentLimit = 0
            self.controlType =  SimpleFOCDevice.ANGLE_CONTROL
            self.torqueType =  SimpleFOCDevice.VOLTAGE_TORQUE
            self.initialTarget = 0
            self.motionDownsample = 0

            # monitor variables
            self.monitorDownsample = 0
            self.monitorVariables = 0

            # state variables
            self.target = 0
            self.stateUpdater = StateUpdateRunner(self)
            self.targetNow = 0
            self.angleNow = 0
            self.velocityNow = 0
            self.voltageQNow = 0
            self.voltageDNow = 0
            self.currentQNow = 0
            self.currentDNow = 0

            # general variables
            self.phaseResistance = 0
            self.deviceStatus = 0
            self.modulationType = 0
            self.modulationCentered = 1

            # sensor variables
            self.sensorElectricalZero = 0
            self.sensorZeroOffset = 0

            # list of custom commands
            self.customCommands = CustomCommands()

            # return the class instance
            SimpleFOCDevice.__instance = self


    def configureDevice(self, jsonValue):
        # motion control parameters
        self.PIDVelocity.load(jsonValue['PIDVelocity'])
        self.PIDAngle.load(jsonValue['PIDAngle'])
        self.PIDCurrentD.load(jsonValue['PIDCurrentD'])
        self.PIDCurrentQ.load(jsonValue['PIDCurrentQ'])
        
        # low pass filters
        self.LPFVelocity.Tf = jsonValue['LPFVelocity']
        self.LPFAngle.Tf = jsonValue['LPFAngle']
        self.LPFCurrentQ.Tf = jsonValue['LPFCurrentQ']
        self.LPFCurrentD.Tf = jsonValue['LPFCurrentD']
        # limit variables
        self.velocityLimit = jsonValue['velocityLimit']
        self.voltageLimit = jsonValue['voltageLimit']
        self.currentLimit = jsonValue['currentLimit']
        # motion control types
        self.controlType = jsonValue['controlType']
        self.torqueType = jsonValue['torqueType']
        self.motionDownsample = jsonValue['motionDownsample']

        # sensor zero offset and electrical zero offset
        self.sensorElectricalZero = jsonValue['sensorElectricalZero']
        self.sensorZeroOffset = jsonValue['sensorZeroOffset']

        # motor phase resistance
        self.phaseResistance = jsonValue['phaseResistance']

        # initial target
        self.initialTarget = jsonValue['initialTarget']
    
        # serial communication variables
        self.connectionID = jsonValue['connectionID']
        self.serialPortName = jsonValue['serialPortName']
        self.serialRate = jsonValue['serialRate']
        self.serialByteSize = jsonValue['serialByteSize']
        self.serialParity = jsonValue['serialParity']
        self.stopBits = jsonValue['stopBits']
        try:
            self.customCommands.customCommandsList = []
            self.customCommands.load(jsonValue['customCommands'])
        except KeyError:
            pass
        try:
            self.devCommandID = jsonValue['devCommandID']
        except KeyError:
            pass

    def configureConnection(self, configDict):
        self.connectionID = configDict['connectionID']
        self.serialPortName = configDict['serialPortName']
        self.serialRate = configDict['serialRate']
        self.serialByteSize = configDict['serialByteSize']
        self.serialParity = configDict['serialParity']
        self.stopBits = configDict['stopBits']

    def toJSON(self):
        valuesToSave = {
            'PIDVelocity': self.PIDVelocity.serialize(),
            'PIDAngle': self.PIDAngle.serialize(),
            'PIDCurrentD': self.PIDCurrentD.serialize(),
            'PIDCurrentQ': self.PIDCurrentQ.serialize(),
            'LPFVelocity':self.LPFVelocity.Tf,
            'LPFAngle':self.LPFAngle.Tf,
            'LPFCurrentD':self.LPFCurrentD.Tf,
            'LPFCurrentQ':self.LPFCurrentQ.Tf,
            'velocityLimit': self.velocityLimit,
            'voltageLimit': self.voltageLimit,
            'currentLimit': self.currentLimit,
            'controlType': self.controlType,
            'motionDownsample':self.motionDownsample,
            'torqueType': self.torqueType,
            'phaseResistance': self.phaseResistance,
            'sensorZeroOffset': self.sensorZeroOffset,
            'sensorElectricalZero': self.sensorElectricalZero,
            'initialTarget': self.initialTarget,
            'connectionID': self.connectionID,
            'serialPortName': self.serialPortName,
            'serialRate': self.serialRate,
            'serialByteSize': self.serialByteSize,
            'serialParity': self.serialParity,
            'stopBits': self.stopBits,
            'devCommandID': self.devCommandID,

        }
        valuesToSave.update(self.customCommands.serialize())
        return valuesToSave

        
    def toArduinoCode(self, generateParams = []):

        # code = "#include <SimpleFOC.h>\n\n"
        # code += "void setup(){\n\n"
        # code += "....\n\n"
        code = "\n"
        if generateParams[0] or generateParams==[]:
            code += "// control loop type and torque mode \n"
            code += "motor.torque_controller = TorqueControlType::"
            if self.torqueType == self.VOLTAGE_TORQUE:
                code += "voltage"
            elif self.torqueType == self.DC_CURRENT_TORQUE:
                code += "dc_current"
            elif self.torqueType == self.FOC_CURRENT_TORQUE:
                code += "foc_current"
            code += ";\n"
            code += "motor.controller = MotionControlType::"
            if self.controlType == self.TORQUE_CONTROL:
                code += "torque"
            elif self.controlType == self.VELOCITY_CONTROL:
                code += "velocity"
            elif self.controlType == self.ANGLE_CONTROL:
                code += "angle"
            elif self.controlType == self.VELOCITY_CONTROL:
                code += "velocity_openloop"
            elif self.controlType == self.ANGLE_CONTROL:
                code += "angle_openloop"
            code += ";\n"
            code += "motor.motion_downsample = " + str(self.motionDownsample) +";\n" 
            code += "\n"

        if generateParams[1] or generateParams==[]:
            code += "// velocity loop PID\n"  
            code += "motor.PID_velocity.P = " + str(self.PIDVelocity.P) +";\n"  
            code += "motor.PID_velocity.I = " + str(self.PIDVelocity.I) +";\n"  
            code += "motor.PID_velocity.D = " + str(self.PIDVelocity.D) +";\n"  
            code += "motor.PID_velocity.output_ramp = " + str(self.PIDVelocity.outputRamp) +";\n"  
            code += "motor.PID_velocity.limit = " + str(self.PIDVelocity.outputLimit) +";\n"  
            code += "// Low pass filtering time constant \n"  
            code += "motor.LPF_velocity.Tf = " + str(self.LPFVelocity.Tf) +";\n"  
        if generateParams[2] or generateParams==[]:
            code += "// angle loop PID\n"
            code += "motor.P_angle.P = " + str(self.PIDAngle.P) +";\n"  
            code += "motor.P_angle.I = " + str(self.PIDAngle.I) +";\n"   
            code += "motor.P_angle.D = " + str(self.PIDAngle.D) +";\n"    
            code += "motor.P_angle.output_ramp = " + str(self.PIDAngle.outputRamp) +";\n"   
            code += "motor.P_angle.limit = " + str(self.PIDAngle.outputLimit) +";\n"  
            code += "// Low pass filtering time constant \n" 
            code += "motor.LPF_angle.Tf = " + str(self.LPFAngle.Tf) +";\n"  
        if generateParams[3] or generateParams==[]: 
            code += "// current q loop PID \n"
            code += "motor.PID_current_q.P = " + str(self.PIDCurrentQ.P) +";\n"  
            code += "motor.PID_current_q.I = " + str(self.PIDCurrentQ.I) +";\n"   
            code += "motor.PID_current_q.D = " + str(self.PIDCurrentQ.D) +";\n"   
            code += "motor.PID_current_q.output_ramp = " + str(self.PIDCurrentQ.outputRamp) +";\n"  
            code += "motor.PID_current_q.limit = " + str(self.PIDCurrentQ.outputLimit) +";\n"  
            code += "// Low pass filtering time constant \n" 
            code += "motor.LPF_current_q.Tf = " + str(self.LPFCurrentQ.Tf) +";\n"  
        if generateParams[4] or generateParams==[]:
            code += "// current d loop PID\n"
            code += "motor.PID_current_d.P = " + str(self.PIDCurrentD.P) +";\n"   
            code += "motor.PID_current_d.I = " + str(self.PIDCurrentD.I) +";\n"  
            code += "motor.PID_current_d.D = " + str(self.PIDCurrentD.D) +";\n"  
            code += "motor.PID_current_d.output_ramp = " + str(self.PIDCurrentD.outputRamp) +";\n"   
            code += "motor.PID_current_d.limit = " + str(self.PIDCurrentD.outputLimit) +";\n"  
            code += "// Low pass filtering time constant \n" 
            code += "motor.LPF_current_d.Tf = " + str(self.LPFCurrentD.Tf) +";\n" 
 
        if generateParams[5] or generateParams==[]:
            code += "// Limits \n"
            code += "motor.velocity_limit = " + str(self.velocityLimit) +";\n" 
            code += "motor.voltage_limit = " + str(self.voltageLimit) +";\n" 
            code += "motor.current_limit = " + str(self.currentLimit) +";\n" 

        if generateParams[6] or generateParams==[]:
            code += "// sensor zero offset - home position \n"
            code += "motor.sensor_offset = " + str(self.sensorZeroOffset) +";\n" 

        if generateParams[7] or generateParams==[]:
            code += "// sensor zero electrical angle \n"
            code += "// this parameter enables skipping a part of initFOC \n"
            code += "motor.sensor_electrical_offset = " + str(self.sensorElectricalZero) +";\n" 

        if generateParams[8] or generateParams==[]:
            code += "// general settings \n"
            code += "// motor phase resistance \n"
            code += "motor.phase_resistance = " + str(self.sensorElectricalZero) +";\n" 
            
        if generateParams[9] or generateParams==[]:
            code += "// pwm modulation settings \n"
            code += "motor.foc_modulation = FOCModulationType::"
            if self.modulationType == self.SINE_PWM:
                code += "SinePWM"
            elif self.modulationType == self.SPACE_VECTOR_PWM:
                code += "SpaceVectorPWM"
            elif self.modulationType == self.TRAPEZOIDAL_120:
                code += "Trapezoid_120"
            elif self.modulationType == self.TRAPEZOIDAL_150:
                code += "Trapezoid_150"
            code += ";\n"
            code += "motor.modulation_centered = " + str(self.modulationCentered) +";\n" 

        # code += "\n\nmotor.init();\nmotor.initFOC();\n\n...\n\n }"
        # code += "\n\nvoid loop() {\n\n....\n\n}"
        
        return code

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
                if self.stateUpdater.stopped():
                    self.stateUpdater = StateUpdateRunner(self)
                self.stateUpdater.start()
            elif connectionMode == SimpleFOCDevice.PUSH_CONFG_ON_CONNECT:
                self.pushConfiguration()
                if self.stateUpdater.stopped():
                    self.stateUpdater = StateUpdateRunner(self)
                self.stateUpdater.start()
                pass
            return True

    def disConnect(self):
        self.isConnected = False
        self.__closeCommunication()
        self.stateUpdater.stop()
        for listener in self.connectionStateListenerList:
            listener.connectionStateChanged(False)

    def addConnectionStateListener(self, listener):
        self.connectionStateListenerList.append(listener)

    def sendCommand(self, command):
        if self.isConnected:
            self.serialPort.write((str(command) + '\n').encode('utf-8'))

    def setCommand(self, command, value):
        if self.isConnected:
           self.sendCommand(str(self.devCommandID) + str(command) + str(value))

    def getCommand(self, command):
        if self.isConnected:
           self.sendCommand(str(self.devCommandID) + str(command) )

    def sendControlType(self, loop_control_type):
        if self.isConnected:
            if loop_control_type  != '':
                self.controlType = loop_control_type    
            self.setCommand('C', str(loop_control_type))
            
    def sendTorqueType(self, torque_type):
        if self.isConnected:
            if torque_type  != '':
                self.torqueType = torque_type    
            self.setCommand('T', str(torque_type))
            
    def sendMotionDownsample(self, value):
        if self.isConnected:
            if value  != '':
                self.motionDownsample = value    
            self.setCommand('CD', str(value))

    def sendProportionalGain(self, pid, value ):
        if self.isConnected:
            if value  != '':
                pid.P = value
            self.setCommand(str(pid.cmd)+'P',  str(value))

    def sendIntegralGain(self, pid, value):
        if self.isConnected:
            if value  != '':
                pid.I = value
            self.setCommand(str(pid.cmd)+'I', str(value))

    def sendDerivativeGain(self, pid,  value):
        if self.isConnected:
            if value  != '':
                pid.D = value
            self.setCommand(str(pid.cmd)+'D', str(value))

    def sendOutputRamp(self, pid, value):
        if self.isConnected:
            if value  != '':
                pid.outputRamp = value
            self.setCommand(str(pid.cmd)+'R', str(value))

    def sendOutputLimit(self, pid, value):
        if self.isConnected:
            if value  != '':
                pid.outputLimit = value
            self.setCommand(str(pid.cmd)+'L', str(value))

    def sendLowPassFilter(self, lpf, value):
        if self.isConnected:
            if value  != '':
                lpf.Tf = value
            self.setCommand(str(lpf.cmd)+'F', str(value))

    def sendVelocityLimit(self, value):
        if self.isConnected:
            if value  != '':
                self.velocityLimit = value
            self.setCommand('LV', str(value))

    def sendVoltageLimit(self, value):
        if self.isConnected:
            if value  != '':
                self.voltageLimit = value
            self.setCommand('LU', str(value))

    def sendCurrentLimit(self, value):
        if self.isConnected:
            if value  != '':
                self.currentLimit = value
            self.setCommand('LC', str(value))

    def sendPhaseResistance(self, value):
        if self.isConnected:
            if value  != '':
                self.phaseResistance = value
            self.setCommand('R', str(value))

    def sendTargetValue(self, targetvalue):
        if self.isConnected:
            if targetvalue  != '':
                self.target = targetvalue
            self.setCommand('',self.target)

    def sendSensorZeroOffset(self, targetvalue):
        if self.isConnected:
            if targetvalue  != '':
                self.sensorZeroOffset = targetvalue
            self.setCommand('SM', str(targetvalue))

    def sendSensorZeroElectrical(self, targetvalue):
        if self.isConnected:
            if targetvalue  != '':
                self.sensorElectricalZero = targetvalue
            self.setCommand('SE', str(targetvalue))

    def sendDeviceStatus(self, targetvalue):
        if self.isConnected:
            if targetvalue != '':
                self.deviceStatus = targetvalue
            self.setCommand('E', str(targetvalue))

            
    def sendModulationCentered(self, targetvalue):
        if self.isConnected:
            if targetvalue != '':
                self.modulationCentered = targetvalue
            self.setCommand('WC', str(targetvalue))
            
    def sendModulationType(self, targetvalue):
        if self.isConnected:
            if targetvalue != '':
                self.modulationType = targetvalue
            self.setCommand('WT', str(targetvalue))
            
    def sendDeviceStatus(self, targetvalue):
        if self.isConnected:
            if targetvalue != '':
                self.deviceStatus = targetvalue
            self.setCommand('E', str(targetvalue))

    def sendMonitorDownsample(self, targetvalue):
        if self.isConnected:
            if targetvalue != '':
                self.monitorDownsample = targetvalue
            self.setCommand('MD', str(targetvalue))

    def sendMonitorClearVariables(self):
        if self.isConnected:
            self.monitorVariables = 0
            self.getCommand('MC')

    def sendMonitorVariables(self, vararray):
        if self.isConnected:
            if vararray != '':
                val = 0
                m  = 10**6
                for var in vararray:
                    val = val+ int(var)*m
                    m = m/10
                self.monitorVariables = vararray
                self.setCommand('MS', "{:07d}".format(int(val)))
            else:
                self.getCommand('MS')


    def updateStates(self):
        if self.isConnected:
            self.getCommand('MG0')
            time.sleep(100 / 1000)
            self.getCommand('MG1')
            time.sleep(100 / 1000)
            self.getCommand('MG2')
            time.sleep(100 / 1000)
            self.getCommand('MG3')
            time.sleep(100 / 1000)
            self.getCommand('MG4')
            time.sleep(100 / 1000)
            self.getCommand('MG5')
            time.sleep(100 / 1000)
            self.getCommand('MG6')
            time.sleep(100 / 1000)


    def pushConfiguration(self):
        print("push")
        # self.sendControlType(self.controlType)
        # self.sendProportionalGain(self.PIDVelocity, self.self)
        # self.sendIntegralGain(self.PIDVelocity, self.integralGainPID)
        # self.sendDerivativeGain(self.PIDVelocity, self.derivativeGainPID)
        # self.sendOutputRamp(self.PIDVelocity, self.voltageRampPID)
        # self.sendLowPassFilter(self.LPFVelocity,self.lowPassFilter)
        # self.sendPGain(self.anglePGain)
        # self.sendVelocityLimit(self.velocityLimit)
        # self.sendVoltageLimit(self.voltageLimit)
        # self.sendTargetValue(self.initialTarget)

    def pullPIDConf(self, pid, lpf):
        self.sendProportionalGain(pid,'')
        time.sleep(5 / 1000)
        self.sendIntegralGain(pid,'')
        time.sleep(5 / 1000)
        self.sendDerivativeGain(pid,'')
        time.sleep(5 / 1000)
        self.sendOutputRamp(pid,'')
        time.sleep(5 / 1000)
        self.sendOutputLimit(pid,'')
        time.sleep(5 / 1000)
        self.sendLowPassFilter(lpf,'')

    def pullConfiguration(self):
        time.sleep(5 / 1000)
        self.sendControlType('')
        time.sleep(5 / 1000)
        self.sendTorqueType('')
        time.sleep(5 / 1000)
        self.pullPIDConf( self.PIDVelocity, self.LPFVelocity)
        time.sleep(5 / 1000)
        self.pullPIDConf( self.PIDAngle, self.LPFAngle)
        time.sleep(5 / 1000)
        self.pullPIDConf( self.PIDCurrentD, self.LPFCurrentD)
        time.sleep(5 / 1000)
        self.pullPIDConf( self.PIDCurrentQ, self.LPFCurrentQ)
        time.sleep(5 / 1000)
        self.sendVelocityLimit('')
        time.sleep(5 / 1000)
        self.sendVoltageLimit('')
        time.sleep(5 / 1000)
        self.sendCurrentLimit('')
        time.sleep(5 / 1000)
        self.sendSensorZeroElectrical('')
        time.sleep(5 / 1000)
        self.sendSensorZeroOffset('')
        time.sleep(5 / 1000)
        self.sendMotionDownsample('')
        time.sleep(5 / 1000)
        self.sendPhaseResistance('')
        time.sleep(5 / 1000)
        self.sendModulationCentered('')
        time.sleep(5 / 1000)
        self.sendModulationCentered('')
        time.sleep(5 / 1000)
        self.sendDeviceStatus('')

    def parsePIDFResponse(self, pid, lpf, comandResponse):
        if 'P' in comandResponse:
            pid.P = float(comandResponse.replace('P: ', ''))
        if 'I' in comandResponse:
            pid.I = float(comandResponse.replace('I: ', ''))
        if 'D' in comandResponse:
            pid.D = float(comandResponse.replace('D: ', ''))
        if 'ramp' in comandResponse:
            val = comandResponse.replace('ramp:', '')
            if 'ovf' in val:
                pid.outputRamp = 0
            else:
                pid.outputRamp = float(comandResponse.replace('ramp:', ''))
        if 'limit' in comandResponse:
            pid.outputLimit = float(comandResponse.replace('limit:', ''))
        if 'Tf' in comandResponse:
            lpf.Tf = float(comandResponse.replace('Tf: ', ''))

    def parseLimitsResponse(self, comandResponse):
        if 'vel:' in comandResponse:
            self.velocityLimit = float(comandResponse.replace('vel:', ''))
        elif 'volt:' in comandResponse:
            self.voltageLimit = float(comandResponse.replace('volt:', ''))
        elif 'curr:' in comandResponse:
            self.currentLimit = float(comandResponse.replace('curr:', ''))

    def parseMotionResponse(self, comandResponse):
        if 'downsample' in comandResponse:
            self.motionDownsample = float(comandResponse.replace('downsample:', ''))
        elif 'torque' in comandResponse:
            self.controlType = 0
        elif 'angle open' in comandResponse:
            self.controlType = 4
        elif 'angle' in comandResponse:
            self.controlType = 2
        elif 'vel open' in comandResponse:
            self.controlType = 3
        elif 'vel' in comandResponse:
            self.controlType = 1
            
    def parsePWMModResponse(self, comandResponse):
        if 'center' in comandResponse:
            self.modulationCentered = float(comandResponse.replace('center:', ''))
        elif 'type' in comandResponse:
            comandResponse = comandResponse.replace('type:', '')
            if 'Sine' in comandResponse:
                self.modulationType = self.SINE_PWM
            elif 'SVPWM' in comandResponse:
                self.modulationType = self.SPACE_VECTOR_PWM
            elif 'Trap 120' in comandResponse:
                self.modulationType = self.TRAPEZOIDAL_120
            elif 'Trap 150' in comandResponse:
                self.modulationType = self.TRAPEZOIDAL_150
            
    def parseTorqueResponse(self, comandResponse):
        if 'volt' in comandResponse:
            self.torqueType = 0
        elif 'dc curr' in comandResponse:
            self.torqueType = 1
        elif 'foc curr' in comandResponse:
            self.torqueType = 2

    def parseSensorResponse(self, comandResponse):
        if 'el. offset' in comandResponse:
            self.sensorElectricalZero = float(comandResponse.replace('el. offset:', ''))
        elif 'offset' in comandResponse:
            self.sensorZeroOffset = float(comandResponse.replace('offset:', ''))

    def parseMonitorResponse(self, comandResponse):
        if 'all' in comandResponse:
            varStr = comandResponse.replace('all:', '')
            states = varStr.rstrip().split('\t', 7)
            self.targetNow = states[0]
            self.voltageQNow = states[1]
            self.voltageDNow = states[2]
            self.currentQNow = states[3]
            self.currentDNow = states[4]
            self.velocityNow = states[5]
            self.angleNow = states[6]
        if 'target' in comandResponse:
            self.targetNow = float(comandResponse.replace('target:', ''))
        elif 'Vq' in comandResponse:
            self.voltageQNow = float(comandResponse.replace('Vq:', ''))
        elif 'Vd' in comandResponse:
            self.voltageDNow = float(comandResponse.replace('Vd:', ''))
        elif 'Cq' in comandResponse:
            self.currentQNow = float(comandResponse.replace('Cq:', ''))
        elif 'Cd' in comandResponse:
            self.currentDNow = float(comandResponse.replace('Cd:', ''))
        elif 'vel' in comandResponse:
            self.velocityNow = float(comandResponse.replace('vel:', ''))
        elif 'angle' in comandResponse:
            self.angleNow = float(comandResponse.replace('angle:', ''))

    def parseResponses(self, comandResponse):
        if 'PID vel' in comandResponse:
            comandResponse = comandResponse.replace('PID vel|', '')
            self.parsePIDFResponse(self.PIDVelocity, self.LPFVelocity, comandResponse)
        elif 'PID angle' in comandResponse:
            comandResponse = comandResponse.replace('PID angle|', '')
            self.parsePIDFResponse(self.PIDAngle, self.LPFAngle, comandResponse)
        elif 'PID curr q' in comandResponse:
            comandResponse = comandResponse.replace('PID curr q|', '')
            self.parsePIDFResponse(self.PIDCurrentQ, self.LPFCurrentQ, comandResponse)
        elif 'PID curr d' in comandResponse:
            comandResponse = comandResponse.replace('PID curr d|', '')
            self.parsePIDFResponse(self.PIDCurrentD, self.LPFCurrentD, comandResponse)
        elif 'Limits' in comandResponse:
            comandResponse = comandResponse.replace('Limits|', '')
            self.parseLimitsResponse(comandResponse)
        elif 'Motion' in comandResponse:
            comandResponse = comandResponse.replace('Motion:', '')
            self.parseMotionResponse(comandResponse)
        elif 'Torque' in comandResponse:
            comandResponse = comandResponse.replace('Torque:', '')
            self.parseTorqueResponse(comandResponse)
        elif 'Sensor' in comandResponse:
            comandResponse = comandResponse.replace('Sensor |', '')
            self.parseSensorResponse(comandResponse)
        elif 'Monitor' in comandResponse:
            comandResponse = comandResponse.replace('Monitor |', '')
            self.parseMonitorResponse(comandResponse)
        elif 'Status' in comandResponse:
            self.deviceStatus = float(comandResponse.replace('Status:', ''))
        elif 'R phase' in comandResponse:
            self.phaseResistance = float(comandResponse.replace('R phase:', ''))
        elif 'PWM Mod' in comandResponse:
            comandResponse = comandResponse.replace('PWM Mod | ', '')
            self.parsePWMModResponse(comandResponse)

    def parseStateResponses(self, comandResponse):
        if 'Monitor' in comandResponse:
            comandResponse = comandResponse.replace('Monitor |', '')
            self.parseMonitorResponse(comandResponse)


class SerialPortReceiveHandler(QtCore.QThread):
    monitoringDataReceived = QtCore.pyqtSignal(list)
    commandDataReceived = QtCore.pyqtSignal(str)
    stateMonitorReceived = QtCore.pyqtSignal(str)
    rawDataReceived = QtCore.pyqtSignal(str)

    def __init__(self, serial_port=None, *args,**kwargs):
        super(SerialPortReceiveHandler, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.serialComm = serial_port

    def handle_received_data(self, data):
        if not data:
            return
            
        if self.isDataReceivedMonitoring(data):
            try:
                v = data.rstrip().split('\t')
                self.monitoringDataReceived.emit(v)
            except ValueError as error:
                logging.error(error, exc_info=True)
                logging.error('data =' + str(data), exc_info=True)
            except IndexError as error:
                logging.error(error, exc_info=True)
                logging.error('data =' + str(data), exc_info=True)
        elif self.isDataReceivedStates(data):
            self.stateMonitorReceived.emit(data.rstrip())
        else:
            self.commandDataReceived.emit(data.rstrip())
        self.rawDataReceived.emit(data.rstrip())

    def isDataReceivedMonitoring(self, data):
        if data[0].isdigit() or data[0] == '-':
            return True
        else:
            return False
            
    def isDataReceivedStates(self, data):
        if 'Monitor' in data:
            return True
        else:
            return False

    def run(self):
        try:
            while not self.stopped():
                if self.serialComm is not None:
                    if self.serialComm.isOpen():
                        reading = self.serialComm.readline()
                        if reading:
                            self.handle_received_data(reading.decode())
        except SerialException as serialException:
            logging.error(serialException, exc_info=True)
        except TypeError as typeError:
            logging.error(typeError, exc_info=True)
        except AttributeError as ae:
            logging.error(ae, exc_info=True)            

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class StateUpdateRunner(QtCore.QThread):

    def __init__(self, connector=None, *args,**kwargs):
        super(StateUpdateRunner, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.deviceConnector = connector
    def run(self):
        try:
            while not self.stopped():
                if self.deviceConnector is not None:
                    if self.deviceConnector.commProvider.serialComm.isOpen():
                        self.deviceConnector.updateStates()
                        time.sleep(1)
        except SerialException as serialException:
            logging.error(serialException, exc_info=True)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
