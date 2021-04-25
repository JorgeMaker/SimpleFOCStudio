from src.simpleFOCConnector import SimpleFOCDevice
import time
if __name__ == '__main__':
    deviceConnector = SimpleFOCDevice.getInstance()
    deviceConnector.serialPortName = 'COM32'
    deviceConnector.serialRate = 115200
    deviceConnector.devCommandID = 'M'

    if deviceConnector.connect(SimpleFOCDevice.ONLY_CONNECT):
        while True:
            deviceConnector.sendControlType(SimpleFOCDevice.ANGLE_CONTROL)
            deviceConnector.sendTargetValue(0)
            time.sleep(2.0)
            deviceConnector.sendTargetValue(3)
            time.sleep(2)
            deviceConnector.sendTargetValue(6)
            time.sleep(2)
            deviceConnector.sendTargetValue(-6)
            time.sleep(2)
            deviceConnector.sendControlType(SimpleFOCDevice.VELOCITY_CONTROL)
            deviceConnector.sendTargetValue(30)
            time.sleep(2)
            deviceConnector.sendTargetValue(-30)
            time.sleep(2)
