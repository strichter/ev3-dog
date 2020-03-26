###############################################################################
# SPDX-License-Identifier: MIT
# Copyright 2020 by EV3 Robo Dog Authros
###############################################################################
"""Main Robo Dog functionality."""
from pybricks import ev3devices, hubs, messaging, parameters, tools
from pybricks.media.ev3dev import SoundFile
from pybricks.parameters import Direction, Port, Stop, Button

import console, constants, leg, rpc, task


class Back:
    name = 'back'

    def __init__(self):
        self.legs = leg.BackLegSet()

    def connect(self):
        self.legs.connect()

    def disconnect(self):
        self.legs.disconnect()


class Dog:

    back = None
    front = None

    def __init__(self, front_brick_name):
        self.brick = hubs.EV3Brick()
        self.front = rpc.RPCClient(front_brick_name)
        self.back = Back()

    def connect(self):
        self.front.connect()
        self.back.connect()

    def disconnect(self):
        self.stand_up(0)
        self.front.disconnect()
        self.back.disconnect()

    def bark(self):
        self.brick.speaker.play_file(SoundFile.DOG_BARK_1)

    def reset(self):
        reset_grp = task.TaskGroup()
        reset_grp.add(self.front.legs.reset)
        reset_grp.add(self.back.legs.reset)
        reset_grp.start()
        reset_grp.join()

    def stand_up(self, pct, speed=constants.DEFAULT_SPEED, wait=True):
        bend_grp = task.TaskGroup()
        bend_grp.add(self.front.legs.stand_up, (pct, speed))
        bend_grp.add(self.back.legs.stand_up, (pct, speed))
        bend_grp.start()
        bend_grp.join()

    def sit(self, speed=constants.DEFAULT_SPEED, wait=True):
        reset_grp = task.TaskGroup()
        # Front goes all the way up.
        reset_grp.add(self.front.legs.stand_up, (100.0, speed))
        # Back goes all the way down.
        reset_grp.add(self.back.legs.stand_up, (0.0, speed))
        reset_grp.start()
        reset_grp.join()

    def lift_paw(self, side, pct, speed=constants.DEFAULT_SPEED, wait=True):
        leg = getattr(self.front.legs, side)
        leg.lift_up(pct, speed, wait)


def main():
    dog = Dog('ev3-dog2')
    dog.connect()
    dog.reset()
    #dog.stand_up(100)
    console.console({'dog': dog})
    #dog.sit()
    #dog.lift_paw('right', 100)
    #dog.lift_paw('right', 0)

    #dog.frontBrick.front.legs.right.upper.stop()
    #dog.frontBrick.front.legs.right.lower.stop()
    #uprev = ucur = None
    #lprev = lcur = None
    #try:
    #    while True:
    #        ucur = dog.frontBrick.front.legs.right.upper.angle()
    #        if ucur != uprev:
    #            print('upper', ucur)
    #            uprev = ucur
    #        lcur = dog.frontBrick.front.legs.right.lower.angle()
    #        if lcur != lprev:
    #            print('lower', lcur)
    #            lprev = lcur
    #        tools.wait(100)
    #except KeyboardInterrupt:
    #    pass
    #except:
    #    dog.disconnect()
    #    reraise

    #sensor = ev3devices.InfraredSensor(Port.S4)
    #try:
    #    while True:
    #        buttons = sensor.keypad()
    #        print(buttons)
    #        if Button.RIGHT_UP in buttons:
    #            dog.bark()
    #        if Button.RIGHT_DOWN in buttons:
    #            dog.sit()
    #        if Button.LEFT_UP in buttons:
    #            dog.stand_up(100)
    #        if Button.LEFT_DOWN in buttons:
    #            dog.stand_up(0)
    #        tools.wait(100)
    #except KeyboardInterrupt:
    #    pass
    #while True:
    #    cmd = input('Cmd: ')
    #    if cmd == 'quit':
    #        break
    #    elif cmd == 'up':
    #        dog.stand_up(100)
    #    elif cmd == 'down':
    #        dog.stand_up(0)
    #    elif cmd == 'sit':
    #        dog.sit()
    #    elif cmd == 'bark':
    #        dog.bark()
    #    elif cmd == 'paw':
    #        dog.give_paw()
    dog.disconnect()


if __name__ == '__main__':
    main()
