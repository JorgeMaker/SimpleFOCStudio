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

        signal0Pen = pg.mkPen(color=GUIToolKit.RED_COLOR, width=2)
        self.signal0Plot = pg.PlotDataItem(self.timeArray,
                                           self.signal0DataArray,
                                           pen=signal0Pen)
        self.plotWidget.addItem(self.signal0Plot)

        signal1Pen = pg.mkPen(color=GUIToolKit.ORANGE_COLOR, width=2)
        self.signal1Plot = pg.PlotDataItem(self.timeArray,
                                           self.signal1DataArray,
                                           pen=signal1Pen)
        self.plotWidget.addItem(self.signal1Plot)

        signal2Pen = pg.mkPen(color=GUIToolKit.GREEN_COLOR, width=2)
        self.signal2Plot = pg.PlotDataItem(self.timeArray,
                                           self.signal2DataArray,
                                           pen=signal2Pen)
        self.plotWidget.addItem(self.signal2Plot)

        self.horizontalLayout.addWidget(self.plotWidget)

        self.controlPlotWidget = ControlPlotPanel(controllePlotWidget=self)
        self.horizontalLayout.addWidget(self.controlPlotWidget)

        self.signal0PlotFlag = True
        self.signal1PlotFlag = True
        self.signal2PlotFlag = True

        self.controlPlotWidget.signal0CheckBox.stateChanged.connect(
            self.signal0PlotFlagUpdate)
        self.controlPlotWidget.signal1CheckBox.stateChanged.connect(
            self.signal1PlotFlagUpdate)
        self.controlPlotWidget.signal2CheckBox.stateChanged.connect(
            self.signal2PlotFlagUpdate)

        self.device.commProvider.telemetryDataReceived.connect(
            self.upDateGraphic)

        self.currentStatus = self.disconnectedState
        self.controlPlotWidget.pauseContinueButton.setDisabled(True)

        self.controlPlotWidget.controlTypeChonged(self.device.controlType)

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

    def signal1PlotFlagUpdate(self):
        if self.controlPlotWidget.signal1CheckBox.isChecked():
            self.signal1PlotFlag = True
            self.plotWidget.addItem(self.signal1Plot)

        else:
            self.signal1PlotFlag = False
            self.plotWidget.removeItem(self.signal1Plot)

    def signal2PlotFlagUpdate(self):
        if self.controlPlotWidget.signal2CheckBox.isChecked():
            self.signal2PlotFlag = True
            self.plotWidget.addItem(self.signal2Plot)
        else:
            self.signal2PlotFlag = False
            self.plotWidget.removeItem(self.signal2Plot)

    def connectioStatusUpdate(self, connectedFlaf):
        if connectedFlaf:
            self.currentStatus = self.initialConnectedState
        else:
            self.currentStatus = self.disconnectedState

    def upDateGraphic(self, signal0, signal1, signal2):
        if self.currentStatus is self.connectedPlottingStartedState or \
                self.currentStatus is self.connectedPausedState:

            if type(signal0) is float and type(signal1) is float and type(
                    signal2) is float:
                self.storeAndShiftData(signal0, signal1, signal2)
                if self.currentStatus is self.connectedPlottingStartedState:
                    self.updatePlot()
            else:
                logging.warning(
                    'Arrived corrupted data: {} {} {}'.format(signal0, signal1,
                                                              signal2))

    def storeAndShiftData(self, signal0, signal1, signal2):

        self.signal0DataArray = np.roll(self.signal0DataArray, -1)
        self.signal0DataArray[-1] = signal0

        self.signal1DataArray = np.roll(self.signal1DataArray, -1)
        self.signal1DataArray[-1] = signal1

        self.signal2DataArray = np.roll(self.signal2DataArray, -1)
        self.signal2DataArray[-1] = signal2

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


class ControlPlotPanel(QtWidgets.QWidget):

    def __init__(self, parent=None, controllePlotWidget=None):
        '''Constructor for ToolsWidget'''
        super().__init__(parent)

        self.device = SimpleFOCDevice.getInstance()
        self.controlledPlot = controllePlotWidget
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName('horizontalLayout')

        self.startStopButton = QtWidgets.QPushButton(self)
        self.startStopButton.setText('Start plotting')
        self.startStopButton.setObjectName('pause')
        self.startStopButton.clicked.connect(self.startStoPlotAction)
        self.startStopButton.setIcon(GUIToolKit.getIconByName('start'))
        self.horizontalLayout.addWidget(self.startStopButton)

        self.pauseContinueButton = QtWidgets.QPushButton(self)
        self.pauseContinueButton.setObjectName('pauseButton')
        self.pauseContinueButton.setText('Pause plotting')
        self.pauseContinueButton.setIcon(GUIToolKit.getIconByName('pause'))
        self.pauseContinueButton.clicked.connect(self.pauseContinuePlotAction)
        self.horizontalLayout.addWidget(self.pauseContinueButton)

        self.zoomAllButton = QtWidgets.QPushButton(self)
        self.zoomAllButton.setObjectName('zoomAllButton')
        self.zoomAllButton.setText('View all plot')
        self.zoomAllButton.setIcon(GUIToolKit.getIconByName('zoomall'))
        self.zoomAllButton.clicked.connect(self.zoomAllPlot)
        self.horizontalLayout.addWidget(self.zoomAllButton)

        self.signal0CheckBox = QtWidgets.QCheckBox(self)
        self.signal0CheckBox.setObjectName('signal0CheckBox')
        self.signal0CheckBox.setText('Signal0')
        self.signal0CheckBox.setIcon(GUIToolKit.getIconByName('reddot'))
        self.signal0CheckBox.setChecked(True)
        self.horizontalLayout.addWidget(self.signal0CheckBox)

        self.signal2CheckBox = QtWidgets.QCheckBox(self)
        self.signal2CheckBox.setText('Signal2')
        self.signal2CheckBox.setIcon(GUIToolKit.getIconByName('greendot'))
        self.signal2CheckBox.setChecked(True)
        self.signal2CheckBox.setObjectName('signal2CheckBox')
        self.horizontalLayout.addWidget(self.signal2CheckBox)

        self.signal1CheckBox = QtWidgets.QCheckBox(self)
        self.signal1CheckBox.setChecked(True)
        self.signal1CheckBox.setText('Signal1')
        self.signal1CheckBox.setIcon(GUIToolKit.getIconByName('orangedot'))
        self.signal1CheckBox.setObjectName('signal1CheckBox')
        self.horizontalLayout.addWidget(self.signal1CheckBox)

        spacerItem = QtWidgets.QSpacerItem(100, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Maximum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.addItem(spacerItem)

        self.device.commProvider.commandDataReceived.connect(
            self.commandResponseReceived)

    def startStoPlotAction(self):
        if self.controlledPlot.currentStatus is self.controlledPlot.initialConnectedState:
            # Start pressed
            self.startStopButton.setText('Stop plotting')
            self.startStopButton.setIcon(GUIToolKit.getIconByName('stop'))
            self.controlledPlot.currentStatus = \
                self.controlledPlot.connectedPlottingStartedState
            self.pauseContinueButton.setEnabled(True)
        else:
            # Stop pressed
            self.startStopButton.setText('Start plotting')
            self.startStopButton.setIcon(GUIToolKit.getIconByName('start'))

            self.pauseContinueButton.setText('Pause plotting')
            self.pauseContinueButton.setIcon(GUIToolKit.getIconByName('pause'))
            self.pauseContinueButton.setEnabled(False)
            self.stopAndResetPlot()

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

    def zoomAllPlot(self):
        self.controlledPlot.plotWidget.enableAutoRange()

    def updateLabels(self, label0, label1, label2):
        self.signal0CheckBox.setText(label0)
        self.signal1CheckBox.setText(label1)
        self.signal2CheckBox.setText(label2)

    def controlTypeChonged(self, controlMode):
        label0, label2, label1 = SimpleFOCDevice.getSignalLabels(controlMode)
        self.updateLabels(label0, label1, label2)

    def commandResponseReceived(self, cmdRespose):
        if 'Control: ' in cmdRespose:
            self.controlTypeChonged(SimpleFOCDevice.getControlModeCode(
                cmdRespose.replace('Control: ', '')))
