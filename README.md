## *Simple**FOC**Studio*

Graphical user interface for the [*Simple**FOC**library*](https://github.com/simplefoc). This application allows to tune and configure any BLDC/Stepper *Simple**FOC**library* controlled device, using serial port communications and the [Commander](https://docs.simplefoc.com/commander_interface) interface.
#### The main features are:
- Plug and play with the *Simple**FOC**library* version 2.1 
- Real-time tuning and configuration of the motors
- Real-time plotting and monitoring of motor variables
- Code generation for easier integration of the tuned parameters in your code
- Built on PyQt5 and a standardized `SimpleFOCConnector` interface that can be used as a gateway form python to the *Simple**FOC**library* device. 

<p align="center">
  <img  src="./DOC/new_gif.gif">
</p>

Add the letter you used to add the motor to the commander interface, in this example ```M```

```command.add(‘M’,doMotor,‘motor’);```

<p align="center">
  <img src="./DOC/treeview.png" width="400px">
  <img src="./DOC/formview.png" width="400px">
</p>

#### Code generation

*Simple**FOC**Studio* helps you to easier transfer your carefully tuned parameters to the Arduino code. Once you are happy with the performance of your system you can automatically generate the arduino code of the parameters you have tuned. To generate the code :
- Click on the <img src="./src/gui/resources/gen.png" height="18"> Arudino button in the toolbar. 
- Choose which sets of parameters you wish to generate the code for and click OK 
- In the new tab you will have a code of your tuned parameters.

The generated code you can just copy/paste in your <code>setup()</code> function, just before calling the <code>motor.init()</code>

<p align="center">
  <img src="./DOC/gen.gif" width="700px">
</p>

#### Integrated serial terminal

*Simple**FOC**Studio* also has integrated serial terminal for easier debugging and monitoring.

<p align="center">
  <img src="./DOC/term.png" width="700px">
</p>

### Arduino code 
Basically there are two things you need to do:
1. Use the commander interface and add the motor to the commander
2. Use the monitoring and add the `motor.monitor()` in the loop

Here is a mockup of the code:

```cpp
#include <SimpleFOC.h>

....

// include commander interface
Commander command = Commander(Serial);
void doMotor(char* cmd) { command.motor(&motor, cmd); }

void setup(){
  ....
  // add the motor to the commander interface
  // The letter (here 'M') you will provide to the SimpleFOCStudio 
  command.add('M',doMotor,'motor');
  // tell the motor to use the monitoring
  motor.useMonitoring(Serial);
  motor.monitor_downsample = 0; // disable monitor at first - optional
  ...

}
void loop(){
  ....

  ....
  // real-time monitoring calls
  motor.monitor();
  // real-time commander calls
  command.run();
}
```
