#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets

from src.gui.sharedcomnponets.sharedcomponets import GUIToolKit
from src.simpleFOCConnector import SimpleFOCDevice


class SimpleFOCGraphicWidget(QtWidgets.QGroupBox):
    disconnectedState = 0
    initialConnectedState = 1
    connectedPausedState = 2
    connectedPlottingStartedState = 3

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName('plotWidget')
        self.setTitle('Real time motor variables: ')
        self.horizontalLayout = QtWidgets.QVBoxLayout(self)
        self.device = SimpleFOCDevice.getInstance()

        self.numberOfSamples = 300

        pg.setConfigOptions(antialias=True)
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.showGrid(x=True, y=True, alpha=0.5)

        self.timeArray = np.arange(-self.numberOfSamples, 0, 1)

        self.signal0DataArray = np.zeros(self.numberOfSamples)
        self.signal1DataArray = np.zeros(self.numberOfSamples)
        self.signal2DataArray = np.zeros(self.numberOfSamples)
        self.signal3DataArray = np.zeros(self.numberOfSamples)
        self.signal4DataArray = np.zeros(self.numberOfSamples)
        self.signal5DataArray = np.zeros(self.numberOfSamples)
        self.signal6DataArray = np.zeros(self.numberOfSamples)

        signal0Pen = pg.mkPen(color=GUIToolKit.RED_COLOR, width=2)
        self.signal0Plot = pg.PlotDataItem(self.timeArray,
                                           self.signal0DataArray,
                                           pen=signal0Pen)
        self.plotWidget.addItem(self.signal0Plot)

        signal1Pen = pg.mkPen(color=GUIToolKit.BLUE_COLOR, width=2)
        self.signal1Plot = pg.PlotDataItem(self.timeArray,
                                           self.signal1DataArray,
                                           pen=signal1Pen)
        self.plotWidget.addItem(self.signal1Plot)

        signal2Pen = pg.mkPen(color=GUIToolKit.PURPLE_COLOR, width=2)
        self.signal2Plot = pg.PlotDataItem(self.timeArray,
                                           self.signal2DataArray,
                                           pen=signal2Pen)
        self.plotWidget.addItem(self.signal2Plot)
        
        signal3Pen = pg.mkPen(color=GUIToolKit.YELLOW_COLOR, width=2)
        self.signal3Plot = pg.PlotDataItem(self.timeArray,
                                           self.signal3DataArray,
                                           pen=signal3Pen)
        self.plotWidget.addItem(self.signal3Plot)

        signal4Pen = pg.mkPen(color=GUIToolKit.MAROON_COLOR, width=2)
        self.signal4Plot = pg.PlotDataItem(self.timeArray,
                                           self.signal4DataArray,
                                           pen=signal4Pen)
        self.plotWidget.addItem(self.signal4Plot)

        signal5Pen = pg.mkPen(color=GUIToolKit.ORANGE_COLOR, width=2)
        self.signal5Plot = pg.PlotDataItem(self.timeArray,
                                           self.signal5DataArray,
                                           pen=signal5Pen)
        self.plotWidget.addItem(self.signal5Plot)

        signal6Pen = pg.mkPen(color=GUIToolKit.GREEN_COLOR, width=2)
        self.signal6Plot = pg.PlotDataItem(self.timeArray,
                                           self.signal6DataArray,
                                           pen=signal6Pen)
        self.plotWidget.addItem(self.signal6Plot)

        self.horizontalLayout.addWidget(self.plotWidget)

        self.controlPlotWidget = ControlPlotPanel(controllerPlotWidget=self)
        self.horizontalLayout.addWidget(self.controlPlotWidget)

        self.signal0PlotFlag = True
        self.signal1PlotFlag = True
        self.signal2PlotFlag = True
        self.signal3PlotFlag = True
        self.signal4PlotFlag = True
        self.signal5PlotFlag = True
        self.signal6PlotFlag = True

        self.controlPlotWidget.signal0CheckBox.stateChanged.connect(
            self.signal0PlotFlagUpdate)
        self.controlPlotWidget.signal1CheckBox.stateChanged.connect(
            self.signal1PlotFlagUpdate)
        self.controlPlotWidget.signal2CheckBox.stateChanged.connect(
            self.signal2PlotFlagUpdate)
        self.controlPlotWidget.signal3CheckBox.stateChanged.connect(
            self.signal3PlotFlagUpdate)
        self.controlPlotWidget.signal4CheckBox.stateChanged.connect(
            self.signal4PlotFlagUpdate)
        self.controlPlotWidget.signal5CheckBox.stateChanged.connect(
            self.signal5PlotFlagUpdate)
        self.controlPlotWidget.signal6CheckBox.stateChanged.connect(
            self.signal6PlotFlagUpdate)

        self.device.commProvider.monitoringDataReceived.connect(
            self.upDateGraphic)

        self.currentStatus = self.disconnectedState
        self.controlPlotWidget.pauseContinueButton.setDisabled(True)

        self.device.addConnectionStateListener(self)

        self.connectionStateChanged(self.device.isConnected)

    def connectionStateChanged(self, deviceConnected):
        if deviceConnected is True:
            self.currentStatus = self.initialConnectedState
            self.enabeUI()
        else:
            self.controlPlotWidget.startStoPlotAction()
            self.controlPlotWidget.stopAndResetPlot()
            self.currentStatus = self.disconnectedState
            self.disableUI()

    def enabeUI(self):
        self.setEnabled(True)

    def disableUI(self):
        self.setEnabled(False)

    def signal0PlotFlagUpdate(self):
        if self.controlPlotWidget.signal0CheckBox.isChecked():
            self.signal0PlotFlag = True
            self.plotWidget.addItem(self.signal0Plot)
        else:
            self.signal0PlotFlag = False
            self.plotWidget.removeItem(self.signal0Plot)
        self.controlPlotWidget.updateMonitorVariables()

    def signal1PlotFlagUpdate(self):
        if self.controlPlotWidget.signal1CheckBox.isChecked():
            self.signal1PlotFlag = True
            self.plotWidget.addItem(self.signal1Plot)
        else:
            self.signal1PlotFlag = False
            self.plotWidget.removeItem(self.signal1Plot)
        self.controlPlotWidget.updateMonitorVariables()

    def signal2PlotFlagUpdate(self):
        if self.controlPlotWidget.signal2CheckBox.isChecked():
            self.signal2PlotFlag = True
            self.plotWidget.addItem(self.signal2Plot)
        else:
            self.signal2PlotFlag = False
            self.plotWidget.removeItem(self.signal2Plot)
        self.controlPlotWidget.updateMonitorVariables()

    def signal3PlotFlagUpdate(self):
        if self.controlPlotWidget.signal3CheckBox.isChecked():
            self.signal3PlotFlag = True
            self.plotWidget.addItem(self.signal3Plot)
        else:
            self.signal3PlotFlag = False
            self.plotWidget.removeItem(self.signal3Plot)
        self.controlPlotWidget.updateMonitorVariables()
            
    def signal4PlotFlagUpdate(self):
        if self.controlPlotWidget.signal4CheckBox.isChecked():
            self.signal4PlotFlag = True
            self.plotWidget.addItem(self.signal4Plot)
        else:
            self.signal4PlotFlag = False
            self.plotWidget.removeItem(self.signal4Plot)
        self.controlPlotWidget.updateMonitorVariables()
            
    def signal5PlotFlagUpdate(self):
        if self.controlPlotWidget.signal5CheckBox.isChecked():
            self.signal5PlotFlag = True
            self.plotWidget.addItem(self.signal5Plot)
        else:
            self.signal5PlotFlag = False
            self.plotWidget.removeItem(self.signal5Plot)
        self.controlPlotWidget.updateMonitorVariables()
            
    def signal6PlotFlagUpdate(self):
        if self.controlPlotWidget.signal6CheckBox.isChecked():
            self.signal6PlotFlag = True
            self.plotWidget.addItem(self.signal6Plot)
        else:
            self.signal6PlotFlag = False
            self.plotWidget.removeItem(self.signal6Plot)
        self.controlPlotWidget.updateMonitorVariables()

    def connectioStatusUpdate(self, connectedFlag):
        if connectedFlag:
            self.currentStatus = self.initialConnectedState
        else:
            self.currentStatus = self.disconnectedState

    def upDateGraphic(self, signalList):
        if self.currentStatus is self.connectedPlottingStartedState or \
                self.currentStatus is self.connectedPausedState:

            signals = np.array(signalList, dtype=float)
            signalIndex = 0

            if bool(self.device.monitorVariables[0]):
                self.signal0DataArray = np.roll(self.signal0DataArray, -1)
                self.signal0DataArray[-1] = signals[signalIndex]
                signalIndex += 1

            if bool(self.device.monitorVariables[1]): 
                self.signal1DataArray = np.roll(self.signal1DataArray, -1)
                self.signal1DataArray[-1] = signals[signalIndex]
                signalIndex += 1

            if bool(self.device.monitorVariables[2]): 
                self.signal2DataArray = np.roll(self.signal2DataArray, -1)
                self.signal2DataArray[-1] = signals[signalIndex]
                signalIndex += 1

            if bool(self.device.monitorVariables[3]): 
                self.signal3DataArray = np.roll(self.signal3DataArray, -1)
                self.signal3DataArray[-1] = signals[signalIndex]
                signalIndex += 1

            if bool(self.device.monitorVariables[4]): 
                self.signal4DataArray = np.roll(self.signal4DataArray, -1)
                self.signal4DataArray[-1] = signals[signalIndex]
                signalIndex += 1

            if bool(self.device.monitorVariables[5]): 
                self.signal5DataArray = np.roll(self.signal5DataArray, -1)
                self.signal5DataArray[-1] = signals[signalIndex]
                signalIndex += 1

            if bool(self.device.monitorVariables[6]): 
                self.signal6DataArray = np.roll(self.signal6DataArray, -1)
                self.signal6DataArray[-1] = signals[signalIndex]

            if self.currentStatus is self.connectedPlottingStartedState:
                self.updatePlot()
                
            else:
                logging.warning(
                    'Arrived corrupted data: {} {} {}'.format(signal0, signal1,
                                                              signal2))


    def computeStatic(self, array):
        mean = np.mean(array)
        std = np.std(array)
        max = np.max(array)
        min = np.min(array)
        meadian = np.median(array)

    def updatePlot(self):
        if self.signal0PlotFlag:
            self.signal0Plot.setData(self.timeArray, self.signal0DataArray)
            self.signal0Plot.updateItems()
            self.signal0Plot.sigPlotChanged.emit(self.signal0Plot)

        if self.signal1PlotFlag:
            self.signal1Plot.setData(self.timeArray, self.signal1DataArray)
            self.signal1Plot.updateItems()
            self.signal1Plot.sigPlotChanged.emit(self.signal1Plot)

        if self.signal2PlotFlag:
            self.signal2Plot.setData(self.timeArray, self.signal2DataArray)
            self.signal2Plot.updateItems()
            self.signal2Plot.sigPlotChanged.emit(self.signal2Plot)

        if self.signal3PlotFlag:
            self.signal3Plot.setData(self.timeArray, self.signal3DataArray)
            self.signal3Plot.updateItems()
            self.signal3Plot.sigPlotChanged.emit(self.signal3Plot)

        if self.signal4PlotFlag:
            self.signal4Plot.setData(self.timeArray, self.signal4DataArray)
            self.signal4Plot.updateItems()
            self.signal4Plot.sigPlotChanged.emit(self.signal4PlotFlag)

        if self.signal5PlotFlag:
            self.signal5Plot.setData(self.timeArray, self.signal5DataArray)
            self.signal5Plot.updateItems()
            self.signal5Plot.sigPlotChanged.emit(self.signal5PlotFlag)

        if self.signal6PlotFlag:
            self.signal6Plot.setData(self.timeArray, self.signal6DataArray)
            self.signal6Plot.updateItems()
            self.signal6Plot.sigPlotChanged.emit(self.signal6PlotFlag)


class ControlPlotPanel(QtWidgets.QWidget):

    def __init__(self, parent=None, controllerPlotWidget=None):
        '''Constructor for ToolsWidget'''
        super().__init__(parent)

        self.device = SimpleFOCDevice.getInstance()
        self.controlledPlot = controllerPlotWidget
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.verticalLayout)

        self.horizontalLayout1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout1.setObjectName('horizontalLayout')

        self.startStopButton = QtWidgets.QPushButton(self)
        self.startStopButton.setText('Start plotting')
        self.startStopButton.setObjectName('pause')
        self.startStopButton.clicked.connect(self.startStoPlotAction)
        self.startStopButton.setIcon(GUIToolKit.getIconByName('start'))
        self.horizontalLayout1.addWidget(self.startStopButton)

        self.pauseContinueButton = QtWidgets.QPushButton(self)
        self.pauseContinueButton.setObjectName('pauseButton')
        self.pauseContinueButton.setText('Pause plotting')
        self.pauseContinueButton.setIcon(GUIToolKit.getIconByName('pause'))
        self.pauseContinueButton.clicked.connect(self.pauseContinuePlotAction)
        self.horizontalLayout1.addWidget(self.pauseContinueButton)

        self.zoomAllButton = QtWidgets.QPushButton(self)
        self.zoomAllButton.setObjectName('zoomAllButton')
        self.zoomAllButton.setText('View all plot')
        self.zoomAllButton.setIcon(GUIToolKit.getIconByName('zoomall'))
        self.zoomAllButton.clicked.connect(self.zoomAllPlot)
        self.horizontalLayout1.addWidget(self.zoomAllButton)

        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName('horizontalLayout')

        self.downsampleLabel = QtWidgets.QLabel(self)
        self.downsampleLabel.setText('Downsample')
        self.downampleValue = QtWidgets.QLineEdit(self.downsampleLabel)
        self.downampleValue.setText("100")
        self.downampleValue.editingFinished.connect(self.changeDownsampling)
        self.horizontalLayout2.addWidget(self.downsampleLabel)
        self.horizontalLayout2.addWidget(self.downampleValue)

        self.signal0CheckBox = QtWidgets.QCheckBox(self)
        self.signal0CheckBox.setObjectName('signal0CheckBox')
        self.signal0CheckBox.setText('Tagret')
        self.signal0CheckBox.setIcon(GUIToolKit.getIconByName('reddot'))
        self.signal0CheckBox.setChecked(True)
        self.horizontalLayout2.addWidget(self.signal0CheckBox)

        self.signal5CheckBox = QtWidgets.QCheckBox(self)
        self.signal5CheckBox.setChecked(True)
        self.signal5CheckBox.setText('Velocity')
        self.signal5CheckBox.setIcon(GUIToolKit.getIconByName('orangedot'))
        self.signal5CheckBox.setObjectName('signal5CheckBox')
        self.horizontalLayout2.addWidget(self.signal5CheckBox)

        self.signal6CheckBox = QtWidgets.QCheckBox(self)
        self.signal6CheckBox.setChecked(True)
        self.signal6CheckBox.setText('Angle')
        self.signal6CheckBox.setIcon(GUIToolKit.getIconByName('greendot'))
        self.signal6CheckBox.setObjectName('signal6CheckBox')
        self.horizontalLayout2.addWidget(self.signal6CheckBox)

        self.signal1CheckBox = QtWidgets.QCheckBox(self)
        self.signal1CheckBox.setText('Voltage Q')
        self.signal1CheckBox.setIcon(GUIToolKit.getIconByName('bluedot'))
        self.signal1CheckBox.setChecked(True)
        self.signal1CheckBox.setObjectName('signal1CheckBox')
        self.horizontalLayout2.addWidget(self.signal1CheckBox)

        self.signal2CheckBox = QtWidgets.QCheckBox(self)
        self.signal2CheckBox.setChecked(True)
        self.signal2CheckBox.setText('Voltage D')
        self.signal2CheckBox.setIcon(GUIToolKit.getIconByName('purpledot'))
        self.signal2CheckBox.setObjectName('signal2CheckBox')
        self.horizontalLayout2.addWidget(self.signal2CheckBox)

        self.signal3CheckBox = QtWidgets.QCheckBox(self)
        self.signal3CheckBox.setObjectName('signal0CheckBox')
        self.signal3CheckBox.setText('Current Q')
        self.signal3CheckBox.setIcon(GUIToolKit.getIconByName('yellowdot'))
        self.signal3CheckBox.setChecked(True)
        self.horizontalLayout2.addWidget(self.signal3CheckBox)

        self.signal4CheckBox = QtWidgets.QCheckBox(self)
        self.signal4CheckBox.setText('Current D')
        self.signal4CheckBox.setIcon(GUIToolKit.getIconByName('maroondot'))
        self.signal4CheckBox.setChecked(True)
        self.signal4CheckBox.setObjectName('signal4CheckBox')
        self.horizontalLayout2.addWidget(self.signal4CheckBox)

        spacerItem = QtWidgets.QSpacerItem(100, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Maximum)

        self.horizontalLayout1.addItem(spacerItem)
        self.horizontalLayout1.addItem(spacerItem)
        self.horizontalLayout2.addItem(spacerItem)
        self.horizontalLayout2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout1)
        self.verticalLayout.addLayout(self.horizontalLayout2)

    def startStoPlotAction(self):
        if self.controlledPlot.currentStatus is self.controlledPlot.initialConnectedState:
            # Start pressed
            self.startStopButton.setText('Stop plotting')
            self.startStopButton.setIcon(GUIToolKit.getIconByName('stop'))
            self.controlledPlot.currentStatus = \
                self.controlledPlot.connectedPlottingStartedState
            self.pauseContinueButton.setEnabled(True)
            self.device.sendMonitorDownsample(int(self.downampleValue.text()))
            self.updateMonitorVariables()
        else:
            # Stop pressed
            self.startStopButton.setText('Start plotting')
            self.startStopButton.setIcon(GUIToolKit.getIconByName('start'))
            self.pauseContinueButton.setText('Pause plotting')
            self.pauseContinueButton.setIcon(GUIToolKit.getIconByName('pause'))
            self.pauseContinueButton.setEnabled(False)
            self.stopAndResetPlot()
            self.device.sendMonitorDownsample(0)
            self.device.sendMonitorClearVariables()

    def pauseContinuePlotAction(self):
        if self.controlledPlot.currentStatus is self.controlledPlot.connectedPausedState:
            # Continue pressed
            self.pauseContinueButton.setText('Pause plotting')
            self.pauseContinueButton.setIcon(GUIToolKit.getIconByName('pause'))
            self.controlledPlot.currentStatus = self.controlledPlot.connectedPlottingStartedState
        else:
            # Pause pressed
            self.pauseContinueButton.setText('Continue plotting')
            self.pauseContinueButton.setIcon(
                GUIToolKit.getIconByName('continue'))
            self.controlledPlot.currentStatus = self.controlledPlot.connectedPausedState

    def stopAndResetPlot(self):
        self.controlledPlot.currentStatus = self.controlledPlot.initialConnectedState
        self.controlledPlot.signal0DataArray = np.zeros(
            self.controlledPlot.numberOfSamples)
        self.controlledPlot.signal1DataArray = np.zeros(
            self.controlledPlot.numberOfSamples)
        self.controlledPlot.signal2DataArray = np.zeros(
            self.controlledPlot.numberOfSamples)
        self.controlledPlot.signal3DataArray = np.zeros(
            self.controlledPlot.numberOfSamples)
        self.controlledPlot.signal4DataArray = np.zeros(
            self.controlledPlot.numberOfSamples)
        self.controlledPlot.signal5DataArray = np.zeros(
            self.controlledPlot.numberOfSamples)
        self.controlledPlot.signal6DataArray = np.zeros(
            self.controlledPlot.numberOfSamples)

    def zoomAllPlot(self):
        self.controlledPlot.plotWidget.enableAutoRange()

    def changeDownsampling(self):
        if  self.controlledPlot.currentStatus == self.controlledPlot.connectedPlottingStartedState:
            self.device.sendMonitorDownsample(int(self.downampleValue.text()))

    def updateMonitorVariables(self):
        self.device.sendMonitorVariables([self.signal0CheckBox.isChecked(), 
                                                self.signal1CheckBox.isChecked(),
                                                 self.signal2CheckBox.isChecked(), 
                                                 self.signal3CheckBox.isChecked(), 
                                                 self.signal4CheckBox.isChecked(), 
                                                 self.signal5CheckBox.isChecked(), 
                                                 self.signal6CheckBox.isChecked()])