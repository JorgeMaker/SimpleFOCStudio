#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QVBoxLayout, QFrame)

from src.gui.configtool.connectionControl import ConnectionControlGroupBox
from src.gui.configtool.controlLoopConfig import ControlLoopGroupBox
from src.gui.configtool.deviceTreeview import DeviceTreeView
from src.gui.configtool.droDisplayWidget import DROGroupBox
from src.simpleFOCConnector import SimpleFOCDevice


class DevicesInspectorTree(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.device = SimpleFOCDevice.getInstance()

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.droWidget = DROGroupBox(self)
        self.layout.addWidget(self.droWidget)

        self.controlLoopMode = ControlLoopGroupBox(self)
        self.layout.addWidget(self.controlLoopMode)


        self.treeView = DeviceTreeView(self)
        self.layout.addWidget(self.treeView)

        self.connectionControl = ConnectionControlGroupBox(self)
        self.layout.addWidget(self.connectionControl)

        self.setMaximumWidth(430)
