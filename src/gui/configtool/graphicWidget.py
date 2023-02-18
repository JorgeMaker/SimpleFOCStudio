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

    signals = ['Target', 'Vq','Vd','Cq','Cd','Vel','Angle']
    signal_tooltip = ['Target', 'Voltage D [Volts]','Voltage D [Volts]','Current Q [miliAmps]','Current D [miliAmps]','Velocity [rad/sec]','Angle [rad]']
    signalColors = [GUIToolKit.RED_COLOR, GUIToolKit.BLUE_COLOR, GUIToolKit.PURPLE_COLOR,GUIToolKit.YELLOW_COLOR, GUIToolKit.MAROON_COLOR, GUIToolKit.ORANGE_COLOR, GUIToolKit.GREEN_COLOR]
    signalIcons = ['reddot', 'bluedot','purpledot', 'yellowdot', 'maroondot', 'orangedot', 'greendot']

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
        self.plotWidget.addLegend()

        # self.legend = pg.LegendItem()
        # self.legend.setParentItem(self.plotWidget)

        self.timeArray = np.arange(-self.numberOfSamples, 0, 1)
        
        self.controlPlotWidget = ControlPlotPanel(controllerPlotWidget=self)

        self.signalDataArrays = []
        self.signalPlots = []
        self.signalPlotFlags = []
        for (sig, sigColor, checkBox, tooltip) in zip(self.signals, self.signalColors,self.controlPlotWidget.signalCheckBox, self.signal_tooltip):
            # define signal plot data array
            self.signalDataArrays.append(np.zeros(self.numberOfSamples))
            # configure signal plot parameters
            signalPen = pg.mkPen(color=sigColor, width=1.5)
            self.signalPlots.append(pg.PlotDataItem(self.timeArray,
                                            self.signalDataArrays[-1],
                                            pen=signalPen, name=tooltip))
            self.plotWidget.addItem(self.signalPlots[-1])

            # is plotted flag
            self.signalPlotFlags.append(True)
            # add callback
            checkBox.stateChanged.connect(self.signalPlotFlagUpdate)

        self.horizontalLayout.addWidget(self.plotWidget)
        self.horizontalLayout.addWidget(self.controlPlotWidget)
        
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

    def signalPlotFlagUpdate(self):
        self.controlPlotWidget.updateMonitorVariables()
        for i, (checkBox, plotFlag) in enumerate(zip(self.controlPlotWidget.signalCheckBox, self.signalPlotFlags)):
            if checkBox.isChecked() and (not plotFlag):
                self.signalPlotFlags[i] = True
                self.plotWidget.addItem( self.signalPlots[i] )
            elif (not checkBox.isChecked()) and plotFlag:
                self.signalPlotFlags[i]  = False
                self.plotWidget.removeItem( self.signalPlots[i] )

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

            enabled = np.where(np.array(self.signalPlotFlags) == True)[0]

            if(len(enabled) != len(signals)):
                logging.warning('Arrived corrupted data')
                return
            else:
                for i, ind in enumerate(enabled):
                    self.signalDataArrays[ind] = np.roll(self.signalDataArrays[ind], -1)
                    self.signalDataArrays[ind][-1] = signals[i]

            if self.currentStatus is self.connectedPlottingStartedState:
                self.updatePlot()


    def computeStatic(self, array):
        mean = np.mean(array)
        std = np.std(array)
        max = np.max(array)
        min = np.min(array)
        meadian = np.median(array)

    def updatePlot(self):
        for i, plotFlag in enumerate(self.signalPlotFlags):
            if plotFlag:
                self.signalPlots[i].setData(self.timeArray, self.signalDataArrays[i])
                self.signalPlots[i].updateItems()
                self.signalPlots[i].sigPlotChanged.emit(self.signalPlots[i])


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
        self.startStopButton.setText('Start')
        self.startStopButton.setObjectName('Start')
        self.startStopButton.clicked.connect(self.startStoPlotAction)
        self.startStopButton.setIcon(GUIToolKit.getIconByName('start'))
        self.horizontalLayout1.addWidget(self.startStopButton)

        self.pauseContinueButton = QtWidgets.QPushButton(self)
        self.pauseContinueButton.setObjectName('pauseButton')
        self.pauseContinueButton.setText('Pause')
        self.pauseContinueButton.setIcon(GUIToolKit.getIconByName('pause'))
        self.pauseContinueButton.clicked.connect(self.pauseContinuePlotAction)
        self.horizontalLayout1.addWidget(self.pauseContinueButton)

        self.zoomAllButton = QtWidgets.QPushButton(self)
        self.zoomAllButton.setObjectName('zoomAllButton')
        self.zoomAllButton.setText('View all')
        self.zoomAllButton.setIcon(GUIToolKit.getIconByName('zoomall'))
        self.zoomAllButton.clicked.connect(self.zoomAllPlot)
        self.horizontalLayout1.addWidget(self.zoomAllButton)

        self.signalCheckBox = []
        for i in range(len(self.controlledPlot.signals)):
            checkBox = QtWidgets.QCheckBox(self)
            checkBox.setObjectName('signalCheckBox'+str(i))
            checkBox.setToolTip(self.controlledPlot.signal_tooltip[i])
            checkBox.setText(self.controlledPlot.signals[i])
            checkBox.setIcon(GUIToolKit.getIconByName(self.controlledPlot.signalIcons[i]))
            checkBox.setChecked(True)
            self.signalCheckBox.append(checkBox)
            self.horizontalLayout1.addWidget(checkBox)


        spacerItem = QtWidgets.QSpacerItem(100, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Maximum)

        self.horizontalLayout1.addItem(spacerItem)
        self.horizontalLayout1.addItem(spacerItem)

        self.downsampleLabel = QtWidgets.QLabel(self)
        self.downsampleLabel.setText('Downsample')
        self.downampleValue = QtWidgets.QLineEdit(self.downsampleLabel)
        self.downampleValue.setText("100")
        self.downampleValue.editingFinished.connect(self.changeDownsampling)
        self.horizontalLayout1.addWidget(self.downsampleLabel)
        self.horizontalLayout1.addWidget(self.downampleValue)

        self.verticalLayout.addLayout(self.horizontalLayout1)

    def startStoPlotAction(self):
        if self.controlledPlot.currentStatus is self.controlledPlot.initialConnectedState:
            # Start pressed
            self.startStopButton.setText('Stop')
            self.startStopButton.setIcon(GUIToolKit.getIconByName('stop'))
            self.controlledPlot.currentStatus = \
                self.controlledPlot.connectedPlottingStartedState
            self.pauseContinueButton.setEnabled(True)
            self.device.sendMonitorDownsample(int(self.downampleValue.text()))
            self.updateMonitorVariables()
        else:
            # Stop pressed
            self.startStopButton.setText('Start')
            self.startStopButton.setIcon(GUIToolKit.getIconByName('start'))
            self.pauseContinueButton.setText('Pause')
            self.pauseContinueButton.setIcon(GUIToolKit.getIconByName('pause'))
            self.pauseContinueButton.setEnabled(False)
            self.stopAndResetPlot()
            self.device.sendMonitorDownsample(0)
            self.device.sendMonitorClearVariables()

    def pauseContinuePlotAction(self):
        if self.controlledPlot.currentStatus is self.controlledPlot.connectedPausedState:
            # Continue pressed
            self.pauseContinueButton.setText('Pause')
            self.pauseContinueButton.setIcon(GUIToolKit.getIconByName('pause'))
            self.controlledPlot.currentStatus = self.controlledPlot.connectedPlottingStartedState
        else:
            # Pause pressed
            self.pauseContinueButton.setText('Continue')
            self.pauseContinueButton.setIcon(
                GUIToolKit.getIconByName('continue'))
            self.controlledPlot.currentStatus = self.controlledPlot.connectedPausedState

    def stopAndResetPlot(self):
        self.controlledPlot.currentStatus = self.controlledPlot.initialConnectedState
        for dataArray in self.controlledPlot.signalDataArrays:
            dataArray = np.zeros(self.controlledPlot.numberOfSamples)

    def zoomAllPlot(self):
        self.controlledPlot.plotWidget.enableAutoRange()

    def changeDownsampling(self):
        if  self.controlledPlot.currentStatus == self.controlledPlot.connectedPlottingStartedState:
            self.device.sendMonitorDownsample(int(self.downampleValue.text()))

    def updateMonitorVariables(self):
        self.device.sendMonitorVariables([self.signalCheckBox[0].isChecked(), 
                                                self.signalCheckBox[1].isChecked(),
                                                 self.signalCheckBox[2].isChecked(), 
                                                 self.signalCheckBox[3].isChecked(), 
                                                 self.signalCheckBox[4].isChecked(), 
                                                 self.signalCheckBox[5].isChecked(), 
                                                 self.signalCheckBox[6].isChecked()])