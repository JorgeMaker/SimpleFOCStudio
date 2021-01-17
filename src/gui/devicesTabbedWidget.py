#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from gui.sharedcomponets import GUIToolKit
from gui.deviceConfigTool import DeviceConfigurationWidget
from simpleFOCConnector import SimpleFOCDevice
import json

class DevicesTabbedWidget(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        """Constructor for ToolsWidget"""
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setObjectName("devicesTabWidget")

        self.devicesConfiguratorsList = []

        self.tabCloseRequested.connect(self.removeTabHandler)

        self.setStyleSheet(
            "QTabBar::close - button { image: url(close.png) subcontrol - position: left; }")
        self.setStyleSheet("QTabBar::tab { height: 30px; width: 150px;}")

    def removeTabHandler(self, index):
        self.devicesConfiguratorsList.pop(index)
        self.removeTab(index)

    def addDevice(self):
        customerManagementTool = DeviceConfigurationWidget()
        self.devicesConfiguratorsList.append(customerManagementTool)
        self.addTab(customerManagementTool,
                    GUIToolKit.getIconByName("motor"), "Device")

    def openDevice(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        filenames = None
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            try:
                with open(filenames[0]) as json_file:
                    configurationInfo = json.load(json_file)
                    sfd = SimpleFOCDevice.fromJSON(configurationInfo)
                    sfd.openedFile = filenames
                    customerManagementTool = DeviceConfigurationWidget(simpleFocConn=sfd)
                    self.devicesConfiguratorsList.append(customerManagementTool)
                    tabName ="Device"
                    if sfd.connectionID is not '':
                        tabName = sfd.connectionID
                    self.addTab(customerManagementTool,
                                GUIToolKit.getIconByName("motor"), tabName)
            except Exception as exception:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText("Error while opening selected file")
                msgBox.setWindowTitle("SimpleFOC ConfigTool")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.exec()

    def saveDevice(self):
        if len(self.devicesConfiguratorsList) > 0:
            currentConfigTool = self.devicesConfiguratorsList[self.currentIndex()]
            if currentConfigTool.device.openedFile is None:
                options = QtWidgets.QFileDialog.Options()
                options |= QtWidgets.QFileDialog.DontUseNativeDialog
                fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                          "Save device configuration",
                                                          "",
                                                          "JSON configuration file (*.json)",
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


    def statisticsDevice(self):
        dlg = StatisticsInspectorDialog()
        dlg.exec_()