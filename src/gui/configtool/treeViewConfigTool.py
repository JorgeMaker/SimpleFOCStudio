#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QVBoxLayout, QSplitter)

from src.gui.configtool.deviceInteractionFrame import DeviceInteractionFrame
from src.gui.configtool.devicesInspectorTree import DevicesInspectorTree
from src.gui.sharedcomnponets.sharedcomponets import (WorkAreaTabWidget,
                                                      GUIToolKit)
from src.simpleFOCConnector import SimpleFOCDevice


class TreeViewConfigTool(WorkAreaTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.device = SimpleFOCDevice.getInstance()

        self.layout = QVBoxLayout(self)

        self.treeViewWidget = DevicesInspectorTree(self)
        self.leftWidget = DeviceInteractionFrame(self)

        self.verticalSplitter = QSplitter(Qt.Horizontal)
        self.verticalSplitter.addWidget(self.treeViewWidget)
        self.verticalSplitter.addWidget(self.leftWidget)

        self.layout.addWidget(self.verticalSplitter)

        self.setLayout(self.layout)

    def getTabIcon(self):
        return GUIToolKit.getIconByName('motor')

    def getTabName(self):
        return self.device.connectionID