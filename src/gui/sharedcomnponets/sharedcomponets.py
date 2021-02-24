#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets, QtCore
from serial.tools import list_ports
import os

class GUIToolKit(object):
    ''' This class is used to provide icons for the rest of the application
        hiding the location of the resources
    '''
    RED_COLOR = (255, 92, 92)
    GREEN_COLOR = (57, 217, 138)
    BLUE_COLOR = (91, 141, 236)
    ORANGE_COLOR = (253, 172, 66)

    @staticmethod
    def getIconByName(icoName):

        file_index = {
            'add': 'add.png',
            'delete': 'delete.png',
            'statistics': 'statistics.png',
            'reddot': 'reddot.png',
            'orangedot': 'orangedot.png',
            'greendot': 'greendot.png',
            'send': 'send.png',
            'zoomall': 'zoomall.png',
            'connect': 'connect.png',
            'continue': 'continue.png',
            'alert': 'alert.png',
            'gear': 'gear.png',
            'generalsettings': 'generalsettings.png',
            'open': 'open.png',
            'loop': 'loop.png',
            'save': 'save.png',
            'stop': 'stop.png',
            'restart': 'continue.png',
            'start': 'start.png',
            'motor': 'motor.png',
            'pause': 'pause.png',
            'disconnect': 'disconnect.png',
            'configure': 'configure.png',
            'pidconfig': 'pidconfig.png',
            'consoletool': 'consoletool.png'
        }
        currentDir = os.path.dirname(__file__)
        icon_path = os.path.join(currentDir, '../resources', file_index[icoName])
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal,
                      QtGui.QIcon.Off)
        return icon


class ConfigQLineEdit(QtWidgets.QLineEdit):
    return_key = 16777220
    updateValue = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        '''Constructor for ToolsWidget'''
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == self.return_key:
            self.updateValue.emit()
        else:
            super().keyPressEvent(event)

class WorkAreaTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        '''Constructor for ToolsWidget'''
        super().__init__(parent)

    def getTabIcon(self):
        raise NotImplemented

    def getTabName(self):
        raise NotImplemented

class SerialPortComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None, snifer=None):
        super().__init__(parent)
        self.addItems(self.getAvailableSerialPortNames())

    def getAvailableSerialPortNames(self):
        portNames = []
        for port in list_ports.comports():
            if port[2] != 'n/a':
                portNames.append(port[0])

        return portNames

    def showPopup(self):
        selectedItem = self.currentText()
        super().clear()
        availableSerialPortNames = self.getAvailableSerialPortNames()
        self.addItems(availableSerialPortNames)
        if selectedItem in availableSerialPortNames:
            self.setCurrentText(selectedItem)
        super().showPopup()
