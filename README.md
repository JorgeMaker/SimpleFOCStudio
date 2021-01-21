### SimpleFOCStudio


A GIU application developed  with Python/PyQt5 to manage and configure any [SimpleFOC](https://github.com/simplefoc)  BLDC controlled device using serial port communications. It as a UI that plots in real time monitored  variables PyQtGraph.

![SimpleFOCStudio](DOC/SimpleFOCStudio.gif?raw=true)


#### Installation and Usage

- Clone the repo or download the zip
- cd to the folder
- run: pip install -r "requirements.txt"
- Open your preferred python IDE and make sure to include gui folder ource roots  
   Example whith PyCharm:  https://www.jetbrains.com/help/pycharm/configuring-project-structure.html
- run:  simpleFOCStudio.py

On the arduino side you must have the SimpleFOC device executing the motor.monitor () function
