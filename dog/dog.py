from pybricks import ev3devices, hubs, messaging, parameters, tools
from pybricks.media.ev3dev import SoundFile
from pybricks.parameters import Direction, Port, Stop, Button

import constants, leg, rpc, task


class Dog:

    backLegs = None
    frontLegs = None

    def __init__(self, front_brick_name):
        self.brick = hubs.EV3Brick()
        self.frontBrick = rpc.RPCClient(front_brick_name)
        self.backLegs = leg.BackLegSet()
        self.frontLegs = self.frontBrick.frontLegs

    def connect(self):
        self.frontBrick.connect()
        self.backLegs.connect()

    def disconnect(self):
        self.reset()
        self.frontBrick.disconnect()
        self.backLegs.disconnect()

    def bark(self):
        self.brick.speaker.play_file(SoundFile.DOG_BARK_1)

    def reset(self):
        reset_grp = task.TaskGroup()
        reset_grp.add(self.frontLegs.reset)
        reset_grp.add(self.backLegs.reset)
        reset_grp.start()
        reset_grp.join()

    def stand_up(self, pct, speed=constants.DEFAULT_SPEED, wait=True):
        bend_grp = task.TaskGroup()
        bend_grp.add(self.frontLegs.stand_up, (pct, speed))
        bend_grp.add(self.backLegs.stand_up, (pct, speed))
        bend_grp.start()
        bend_grp.join()

    def sit(self, speed=constants.DEFAULT_SPEED, wait=True):
        reset_grp = task.TaskGroup()
        # Front goes all the way up.
        reset_grp.add(self.frontLegs.stand_up, (100.0, speed))
        # Back goes all the way down.
        reset_grp.add(self.backLegs.stand_up, (0.0, speed))
        reset_grp.start()
        reset_grp.join()

    def lift_paw(self, side, pct, speed=constants.DEFAULT_SPEED, wait=True):
        leg = getattr(self.frontLegs, side)
        leg.lift_up(pct, speed, wait)


def main():
    dog = Dog('ev3-dog2')
    dog.connect()
    dog.reset()
    #dog.stand_up(100)
    dog.sit()
    dog.lift_paw('right', 100)
    input('Done?')
    dog.lift_paw('right', 0)

    #dog.frontBrick.frontLegs.right.upper.stop()
    #dog.frontBrick.frontLegs.right.lower.stop()
    #uprev = ucur = None
    #lprev = lcur = None
    #try:
    #    while True:
    #        ucur = dog.frontBrick.frontLegs.right.upper.angle()
    #        if ucur != uprev:
    #            print('upper', ucur)
    #            uprev = ucur
    #        lcur = dog.frontBrick.frontLegs.right.lower.angle()
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
