from pybricks.ev3devices import InfraredSensor
from pybricks.parameters import Port
from pybricks.tools import print, wait


sensor = InfraredSensor(Port.S4)

while True:
    buttons = sensor.keypad()
    print(buttons)
    wait(1000)
