#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QSyntaxHighlighter,QTextCharFormat,QBrush,QColor)
from PyQt5.QtWidgets import (QVBoxLayout)

from src.gui.sharedcomnponets.sharedcomponets import (WorkAreaTabWidget,
                                                      GUIToolKit)
from src.simpleFOCConnector import SimpleFOCDevice


class GenerateCodeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Generate Code")
        self.setWindowIcon(GUIToolKit.getIconByName('gen'))

        self.checkBoxMotionControl = QtWidgets.QCheckBox(self)
        self.checkBoxMotionControl.setObjectName('motion')
        self.checkBoxMotionControl.setText("Torque/Motion control")
        self.checkBoxMotionControl.setIcon(GUIToolKit.getIconByName('motor'))
        self.checkBoxMotionControl.setChecked(True)

        self.checkBoxPidVel = QtWidgets.QCheckBox(self)
        self.checkBoxPidVel.setObjectName('pidVel')
        self.checkBoxPidVel.setText("PID velocity")
        self.checkBoxPidVel.setIcon(GUIToolKit.getIconByName('pidconfig'))
        self.checkBoxPidVel.setChecked(True)
        
        self.checkBoxPidAngle = QtWidgets.QCheckBox(self)
        self.checkBoxPidAngle.setObjectName('pidAngle')
        self.checkBoxPidAngle.setText("PID angle")
        self.checkBoxPidAngle.setIcon(GUIToolKit.getIconByName('pidconfig'))
        self.checkBoxPidAngle.setChecked(True)
        
        self.checkBoxPidCq = QtWidgets.QCheckBox(self)
        self.checkBoxPidCq.setObjectName('pidCq')
        self.checkBoxPidCq.setText("PID current q")
        self.checkBoxPidCq.setIcon(GUIToolKit.getIconByName('pidconfig'))
        self.checkBoxPidCq.setChecked(True)
        
        self.checkBoxPidCd = QtWidgets.QCheckBox(self)
        self.checkBoxPidCd.setObjectName('pidCq')
        self.checkBoxPidCd.setText("PID current d")
        self.checkBoxPidCd.setIcon(GUIToolKit.getIconByName('pidconfig'))
        self.checkBoxPidCd.setChecked(True)
        
        self.checkBoxLimits = QtWidgets.QCheckBox(self)
        self.checkBoxLimits.setObjectName('limits')
        self.checkBoxLimits.setText("Limits")
        self.checkBoxLimits.setIcon(GUIToolKit.getIconByName('statistics'))
        self.checkBoxLimits.setChecked(True)
        
        self.checkBoxPhaseRes = QtWidgets.QCheckBox(self)
        self.checkBoxPhaseRes.setObjectName('phaseRes')
        self.checkBoxPhaseRes.setText("Phase Resistance")
        self.checkBoxPhaseRes.setIcon(GUIToolKit.getIconByName('res'))
        self.checkBoxPhaseRes.setChecked(True)
        
        self.checkBoxModulation = QtWidgets.QCheckBox(self)
        self.checkBoxModulation.setObjectName('modulation')
        self.checkBoxModulation.setText("PWM Modulation")
        self.checkBoxModulation.setIcon(GUIToolKit.getIconByName('gear'))
        self.checkBoxModulation.setChecked(True)
        
        self.sensorOffset = QtWidgets.QCheckBox(self)
        self.sensorOffset.setObjectName('sensorOffset')
        self.sensorOffset.setText("Sensor Offset")
        self.sensorOffset.setIcon(GUIToolKit.getIconByName('gear'))
        self.sensorOffset.setChecked(True)

        self.sensorElOffset = QtWidgets.QCheckBox(self)
        self.sensorElOffset.setObjectName('sensorOffset')
        self.sensorElOffset.setToolTip('Be careful!<br> Only for absolute sensors')
        self.sensorElOffset.setText("Sensor Electrical Offset")
        self.sensorElOffset.setIcon(GUIToolKit.getIconByName('gear'))
        self.sensorElOffset.setChecked(False)

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        text = "<h1>Arduino Code Generation</h1>"
        text += "Arduino code generation for the motor parameters currently used in the <i>Simple<b>FOC</b>Studio</i> <br>"
        text += "Once you are happy with the performance of your system you can generate the arduino code of the parameters you have tuned.<br>"
        text += "The generated code you can just copy/paste in your <code>setup()</code> function, just before calling the <code>motor.init()</code><br>"
        text += "<h4>Choose the parameter sets to be generated:</h4>"

        self.layout = QtWidgets.QVBoxLayout()
        message1 = QtWidgets.QLabel(text)
        self.layout.addWidget(message1)
        self.layout.addWidget(self.checkBoxMotionControl)
        self.layout.addWidget(self.checkBoxPidVel)
        self.layout.addWidget(self.checkBoxPidAngle)
        self.layout.addWidget(self.checkBoxPidCq)
        self.layout.addWidget(self.checkBoxPidCd)
        self.layout.addWidget(self.checkBoxLimits)
        self.layout.addWidget(self.checkBoxPhaseRes)
        self.layout.addWidget(self.checkBoxModulation)
        self.layout.addWidget(self.sensorOffset)
        self.layout.addWidget(self.sensorElOffset)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class GeneratedCodeDisplay(WorkAreaTabWidget):

    def __init__(self, parent=None ):
        super().__init__(parent)
        
        self.device = SimpleFOCDevice.getInstance()
        dlg = GenerateCodeDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if dlg.exec_():
            toGenerate=[
                dlg.checkBoxMotionControl.isChecked(),
                dlg.checkBoxPidVel.isChecked(),
                dlg.checkBoxPidAngle.isChecked(),
                dlg.checkBoxPidCq.isChecked(),
                dlg.checkBoxPidCd.isChecked(),
                dlg.checkBoxLimits.isChecked(),
                dlg.sensorOffset.isChecked(),
                dlg.sensorElOffset.isChecked(),
                dlg.checkBoxPhaseRes.isChecked(),
                dlg.checkBoxModulation.isChecked(),
            ]
            code = self.device.toArduinoCode(toGenerate)

        self.layout = QVBoxLayout(self)

        text = "<h1>Generated Arduino Code</h1>"
        text += "This generated code you can just copy/paste into your <code>setup()</code> function, it is important that you place it before calling the <code>motor.init()</code><br>"

        message1 = QtWidgets.QLabel(text)
        self.layout.addWidget(message1)

        self.codeDisplayBefore = QtWidgets.QLabel(self)
        self.layout.addWidget(self.codeDisplayBefore)
        code0 = '<font color="#5e6d03">#include</font> <font color="#434f54">&lt;</font><b><font color="#d35400">SimpleFOC</font></b><font color="#434f54">.</font><font color="#000000">h</font><font color="#434f54">&gt;</font>'
        code0 +="<br>...<br>"
        code0 += '<font color="#00979c">void</font> <font color="#5e6d03">setup</font><font color="#000000">(</font><font color="#000000">)</font> <font color="#000000">{</font><br>'
        code0 += "  ...."
        self.codeDisplayBefore.setText(code0)
        self.codeDisplayBefore.setTextFormat(Qt.TextFormat.RichText)

        self.codeDisplay = QtWidgets.QTextEdit(self)
        self.codeDisplay.setObjectName('codeDisplay')
        self.codeDisplay.setText(code)

        highlighter = MyHighlighter( self.codeDisplay, "Classic" )
        self.layout.addWidget(self.codeDisplay)

        self.codeDisplayAfter = QtWidgets.QLabel(self)
        self.layout.addWidget(self.codeDisplayAfter)
        code1 = '<font color="#434f54">&#47;&#47; initialize motor</font><br>'
        code1 += '<font color="#d35400">motor</font><font color="#434f54">.</font><font color="#d35400">init</font><font color="#000000">(</font><font color="#000000">)</font><font color="#000000">;</font><br>'
        code1 += '<font color="#434f54">&#47;&#47; align sensor and start FOC</font><br>'
        code1 += '<font color="#d35400">motor</font><font color="#434f54">.</font><font color="#d35400">initFOC</font><font color="#000000">(</font><font color="#000000">)</font><font color="#000000">;</font><br> ...<br> }'
        code1 += '<br><font color="#00979c">void</font> <font color="#5e6d03">loop</font><font color="#000000">(</font><font color="#000000">)</font> <font color="#000000">{</font>'
        code1 += '<br> .... <br>'
        code1 += '<font color="#d35400">motor</font><font color="#434f54">.</font><font color="#d35400">move</font><font color="#000000">(</font><font color="#000000">)</font><font color="#000000">;</font><br>'
        code1 += '<font color="#d35400">motor</font><font color="#434f54">.</font><font color="#d35400">loopFOC</font><font color="#000000">(</font><font color="#000000">)</font><font color="#000000">;</font><br>'
        code1 += '.... <br>}'
        # MyHighlighter( self.codeDisplayAfter, "Classic" )
        self.codeDisplayAfter.setText(code1)
        self.codeDisplayAfter.setTextFormat(Qt.TextFormat.RichText)

        self.setLayout(self.layout)

    def getTabIcon(self):
        return GUIToolKit.getIconByName('gen')

    def getTabName(self):
        return 'Generated Code'


class MyHighlighter( QSyntaxHighlighter ):

    def __init__( self, parent, theme ):
      QSyntaxHighlighter.__init__( self, parent )
      self.parent = parent
      keyword = QTextCharFormat()
      comment = QTextCharFormat()

      self.highlightingRules = []

      # keyword
      brush = QBrush(QColor(211,84,0), Qt.SolidPattern )
      keyword.setForeground( brush )
      keywords = list( [ "motor",'FOCModulationType','MotionControlType','TorqueControlType'] )
      for word in keywords:
        pattern = QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, keyword )
        self.highlightingRules.append( rule )

      # comment
      brush = QBrush( Qt.gray, Qt.SolidPattern )
      pattern = QRegExp( "\/\/.*[^\n]" )
      comment.setForeground( brush )
      comment.setFontItalic( True )
      rule = HighlightingRule( pattern, comment )
      self.highlightingRules.append( rule )


    def highlightBlock( self, text ):
      for rule in self.highlightingRules:
        expression = QRegExp( rule.pattern )
        index = expression.indexIn( text )
        while index >= 0:
          length = expression.matchedLength()
          self.setFormat( index, length, rule.format )
          index = expression.indexIn( text, index + length )
      self.setCurrentBlockState( 0 )

class HighlightingRule():
  def __init__( self, pattern, format ):
    self.pattern = pattern
    self.format = format
