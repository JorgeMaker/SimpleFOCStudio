#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from PyQt5 import QtWidgets
from src.gui.commandlinetool.commandlinetool import CommandLineConsoleTool
from src.gui.configtool.deviceConfigurationTool import DeviceConfigurationTool
from src.gui.configtool.generatedCodeDisplay import GeneratedCodeDisplay
from src.gui.configtool.treeViewConfigTool import TreeViewConfigTool
from src.simpleFOCConnector import SimpleFOCDevice


class WorkAreaTabbedWidget(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setObjectName('devicesTabWidget')

        self.device = SimpleFOCDevice.getInstance()

        self.cmdLineTool = None
        self.configDeviceTool = None
        self.generatedCodeTab = None
        self.activeToolsList = []

        self.tabCloseRequested.connect(self.removeTabHandler)

        self.setStyleSheet(
            'QTabBar::close - button { image: url(close.png) subcontrol - position: left; }')
        self.setStyleSheet('QTabBar::tab { height: 30px; width: 150px;}')

    def removeTabHandler(self, index):
        if type(self.currentWidget()) == CommandLineConsoleTool:
            self.cmdLineTool = None
        if type(self.currentWidget()) == DeviceConfigurationTool or type(
                self.currentWidget()) == TreeViewConfigTool:
            self.configDeviceTool = None
        if type(self.currentWidget()) == GeneratedCodeDisplay:
            self.generatedCodeTab = None
        if self.configDeviceTool == None and self.cmdLineTool == None:
            if self.device.isConnected:
                self.device.disConnect()

        self.activeToolsList.pop(index)
        self.removeTab(index)

    def addDeviceForm(self):
        if self.configDeviceTool is None:
            self.configDeviceTool = DeviceConfigurationTool()
            self.activeToolsList.append(self.configDeviceTool)
            self.addTab(self.configDeviceTool,
                        self.configDeviceTool.getTabIcon(), 'Device')
            self.setCurrentIndex(self.currentIndex() + 1)
            
    def addDeviceTree(self):
        if self.configDeviceTool is None:
            self.configDeviceTool = TreeViewConfigTool()
            self.activeToolsList.append(self.configDeviceTool)
            self.addTab(self.configDeviceTool,
                        self.configDeviceTool.getTabIcon(), 'Device')
            self.setCurrentIndex(self.currentIndex() + 1)

    def openDevice(self):
        if self.configDeviceTool is None:
            dlg = QtWidgets.QFileDialog()
            dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
            filenames = None
            if dlg.exec_():
                filenames = dlg.selectedFiles()
                try:
                    with open(filenames[0]) as json_file:
                        configurationInfo = json.load(json_file)
                        sfd = SimpleFOCDevice.getInstance()
                        sfd.configureDevice(configurationInfo)
                        self.configDeviceTool = TreeViewConfigTool()
                        sfd.openedFile = filenames
                        self.activeToolsList.append(self.configDeviceTool)
                        tabName = self.configDeviceTool.getTabName()
                        if tabName == '':
                            tabName = 'Device'
                        self.addTab(self.configDeviceTool,
                                    self.configDeviceTool.getTabIcon(), tabName)
                        self.setCurrentIndex(self.currentIndex() + 1)

                except Exception as exception:
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                    msgBox.setText('Error while opening selected file')
                    msgBox.setWindowTitle('SimpleFOC configDeviceTool')
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msgBox.exec()

    def saveDevice(self):
        if len(self.activeToolsList) > 0:
            currentconfigDeviceTool = self.activeToolsList[self.currentIndex()]
            if currentconfigDeviceTool.device.openedFile is None:
                options = QtWidgets.QFileDialog.Options()
                options |= QtWidgets.QFileDialog.DontUseNativeDialog
                fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                    'Save device configuration',
                                                                    '',
                                                                    'JSON configuration file (*.json)',
                                                                    options=options)
                if fileName:
                    self.saveToFile(currentconfigDeviceTool.device, fileName)
            else:
                self.saveToFile(currentconfigDeviceTool.device,
                                currentconfigDeviceTool.device.openedFile)
                                
    def generateCode(self):
        if len(self.activeToolsList) > 0:
            currentconfigDeviceTool = self.activeToolsList[self.currentIndex()]
            self.generatedCodeTab = GeneratedCodeDisplay()
            self.activeToolsList.append(self.generatedCodeTab)
            self.addTab(self.generatedCodeTab,
                        self.generatedCodeTab.getTabIcon(), self.generatedCodeTab.getTabName())
            self.setCurrentIndex(self.currentIndex() + 1)


    def saveToFile(self, deviceToSave, file):
        if type(file) is list:
            with open(file[0], 'w', encoding='utf-8') as f:
                f.write(json.dumps(deviceToSave.toJSON(), indent=4, sort_keys=True))
        else:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(deviceToSave.toJSON(), indent=4, sort_keys=True))

    def openConsoleTool(self):
        if self.cmdLineTool is None:
            self.cmdLineTool = CommandLineConsoleTool()
            self.activeToolsList.append(self.cmdLineTool)
            self.addTab(self.cmdLineTool,
                        self.cmdLineTool.getTabIcon(), 'Cmd Line')
            self.setCurrentIndex(self.currentIndex() + 1)
