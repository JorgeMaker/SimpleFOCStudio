#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from PyQt5 import QtWidgets

from src.gui.configtool.deviceConfigurationTool import DeviceConfigurationTool
from src.gui.commandlinetool.commandlinetool import CommandLineConsoleTool
from src.simpleFOCConnector import SimpleFOCDevice


class WorkAreaTabbedWidget(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setObjectName('devicesTabWidget')

        self.device = SimpleFOCDevice.getInstance()

        self.cmdLineTool = None
        self.configTool = None
        self.activeToolsList = []

        self.tabCloseRequested.connect(self.removeTabHandler)

        self.setStyleSheet(
            'QTabBar::close - button { image: url(close.png) subcontrol - position: left; }')
        self.setStyleSheet('QTabBar::tab { height: 30px; width: 150px;}')

    def removeTabHandler(self, index):
        if type(self.currentWidget()) == CommandLineConsoleTool:
            self.cmdLineTool = None
        if type(self.currentWidget()) == DeviceConfigurationTool:
            self.configTool = None
        if self.configTool == None and self.cmdLineTool == None:
            if self.device.isConnected:
                self.device.disConnect()

        self.activeToolsList.pop(index)
        self.removeTab(index)

    def addDevice(self):
        if self.configTool is None:
            self.configTool = DeviceConfigurationTool(simpleFocConn=self.device)
            self.activeToolsList.append(self.configTool)
            self.addTab(self.configTool,
                        self.configTool.getTabIcon(), 'Device')
            self.setCurrentIndex(self.currentIndex() + 1)

    def openDevice(self):
        if self.configTool is None:
            dlg = QtWidgets.QFileDialog()
            dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
            filenames = None
            if dlg.exec_():
                filenames = dlg.selectedFiles()
                try:
                    with open(filenames[0]) as json_file:
                        configurationInfo = json.load(json_file)
                        sfd = SimpleFOCDevice.getInstance()
                        sfd.configueDevice(configurationInfo)
                        self.configTool = DeviceConfigurationTool(simpleFocConn=sfd)
                        self.configTool.connectionControl.connectionModeComboBox.setCurrentText(SimpleFOCDevice.PUSH_CONFG_ON_CONNECT)

                        sfd.openedFile = filenames
                        self.activeToolsList.append(self.configTool)
                        tabName = self.configTool.getTabName()
                        if tabName == '':
                            tabName = 'Device'
                        self.addTab(self.configTool,
                             self.configTool.getTabIcon(), tabName)
                        self.setCurrentIndex(self.currentIndex() + 1)
                except Exception as exception:
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                    msgBox.setText('Error while opening selected file')
                    msgBox.setWindowTitle('SimpleFOC ConfigTool')
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msgBox.exec()

    def saveDevice(self):
        if len(self.activeToolsList) > 0:
            currentConfigTool = self.activeToolsList[self.currentIndex()]
            if currentConfigTool.device.openedFile is None:
                options = QtWidgets.QFileDialog.Options()
                options |= QtWidgets.QFileDialog.DontUseNativeDialog
                fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                          'Save device configuration',
                                                          '',
                                                          'JSON configuration file (*.json)',
                                                          options=options)
                if fileName:
                    self.saveToFile(currentConfigTool.device, fileName)
            else:
                self.saveToFile(currentConfigTool.device,currentConfigTool.device.openedFile)

    def saveToFile(self, deviceToSave, file):
        if type(file) is list:
            with open(file[0], 'w', encoding='utf-8') as f:
                f.write(json.dumps(deviceToSave.toJSON()))
        else:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(deviceToSave.toJSON()))

    def openConsoleTool(self):
        if self.cmdLineTool is None:
            self.cmdLineTool = CommandLineConsoleTool()
            self.activeToolsList.append(self.cmdLineTool)
            self.addTab(self.cmdLineTool,
                        self.cmdLineTool.getTabIcon(), 'Cmd Line')
            self.setCurrentIndex(self.currentIndex()+1)