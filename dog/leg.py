###############################################################################
# SPDX-License-Identifier: MIT
# Copyright 2020 by EV3 Robo Dog Authros
###############################################################################
"""Robo Dog Leg and Leg Set."""
import math

from pybricks import ev3devices, tools
from pybricks.parameters import Direction, Port

import constants, task


class Leg:

    UPPER_DIRECTION = None
    UPPER_GEARS = None
    LOWER_DIRECTION = None
    LOWER_GEARS = None

    UPRIGHT_UPPER_ANGLE = None
    UPRIGHT_LOWER_ANGLE = None

    name = None
    upper = None
    lower = None

    def __init__(self, name, upper_port, lower_port):
        self.name = name
        self.upper_port = upper_port
        self.lower_port = lower_port

    def connect(self):
        self.upper = ev3devices.Motor(
            self.upper_port, self.UPPER_DIRECTION, self.UPPER_GEARS)
        self.lower = ev3devices.Motor(
            self.lower_port, self.LOWER_DIRECTION, self.LOWER_GEARS)

    def disconnect(self):
        pass

    def _get_speed_ratios(self, upper_target, lower_target):
        upper_delta = math.fabs(upper_target - self.upper.angle())
        lower_delta = math.fabs(lower_target - self.lower.angle())
        ratio = upper_delta / lower_delta if lower_delta else 1.0
        return (ratio, 1.0) if ratio < 1.0 else (1.0, ratio)

    def reset(self):
        self.upper.stop()
        self.upper.control.limits(actuation=constants.RESET_DUTY)
        self.lower.stop()
        self.lower.control.limits(actuation=constants.RESET_DUTY)
        self.upper.run(constants.RESET_SPEED)
        self.lower.run(constants.RESET_SPEED)
        # Stall detection.
        while (not self.upper.control.stalled() or
               not self.lower.control.stalled()):
            tools.wait(constants.DEFAULT_WAIT_TIME)
        # Stop all motors
        self.upper.stop()
        self.upper.control.limits(actuation=100)
        self.lower.stop()
        self.lower.control.limits(actuation=100)
        # Reset angles, so that absolute angles can be used later.
        self.upper.hold()
        self.upper.reset_angle(0)
        self.lower.hold()
        self.lower.reset_angle(0)

    def stand_up(self, pct, speed=constants.DEFAULT_SPEED, wait=True):
        if not (0.0 <= pct <= 100.0):
            raise ValueError('Value out of range: %d%%' % pct)
        # Calculate the angles to bend to.
        upper_target = self.MAX_UPRIGHT_UPPER_ANGLE * pct/100
        lower_target = self.MAX_UPRIGHT_LOWER_ANGLE * pct/100
        # Setup a speed ratio, so that both finish at the same time.
        upper_ratio, lower_ratio = self._get_speed_ratios(
            upper_target, lower_target)
        # Implement our own wait() so we can run th etwo motors in the same
        # thread.
        self.upper.run_target(speed*upper_ratio, upper_target, wait=False)
        self.lower.run_target(speed*lower_ratio, lower_target, wait=False)
        if wait:
            while (not self.upper.control.done() or
                   not self.lower.control.done()):
                tools.wait(constants.DEFAULT_WAIT_TIME)

    def lift_up(self, pct, speed=constants.DEFAULT_SPEED, wait=True):
        if not (0.0 <= pct <= 100.0):
            raise ValueError('Value out of range: %d%%' % pct)
        # Calculate the angles to bend to.
        upper_angle = (
            self.MAX_UPRIGHT_UPPER_ANGLE +
            self.MAX_LIFTUP_UPPER_ANGLE * pct/100
        )
        lower_angle = (
            self.MAX_UPRIGHT_LOWER_ANGLE +
            self.MAX_LIFTUP_LOWER_ANGLE * pct/100
        )
        # Setup a speed ratio, so that both finish at the same time.
        if lower_angle:
            ratio = upper_angle / lower_angle
        else:
            ratio = 1.0
        # Implement our own wait() so we can run th etwo motors in the same
        # thread.
        self.upper.run_target(speed*ratio, upper_angle, wait=False)
        self.lower.run_target(speed, lower_angle, wait=False)
        if wait:
            while (not self.upper.control.done() or
                   not self.lower.control.done()):
                tools.wait(constants.DEFAULT_WAIT_TIME)


class FrontLeg(Leg):

    UPPER_DIRECTION = constants.FRONT_UPPER_DIRECTION
    UPPER_GEARS = constants.FRONT_UPPER_GEARS
    LOWER_DIRECTION = constants.FRONT_LOWER_DIRECTION
    LOWER_GEARS = constants.FRONT_LOWER_GEARS

    MAX_UPRIGHT_UPPER_ANGLE = constants.FRONT_MAX_UPRIGHT_UPPER_ANGLE
    MAX_UPRIGHT_LOWER_ANGLE = constants.FRONT_MAX_UPRIGHT_LOWER_ANGLE

    MAX_LIFTUP_UPPER_ANGLE = constants.FRONT_MAX_LIFTUP_UPPER_ANGLE
    MAX_LIFTUP_LOWER_ANGLE = constants.FRONT_MAX_LIFTUP_LOWER_ANGLE


class BackLeg(Leg):

    UPPER_DIRECTION = constants.BACK_UPPER_DIRECTION
    UPPER_GEARS = constants.BACK_UPPER_GEARS
    LOWER_DIRECTION = constants.BACK_LOWER_DIRECTION
    LOWER_GEARS = constants.BACK_LOWER_GEARS

    MAX_UPRIGHT_UPPER_ANGLE = constants.BACK_MAX_UPRIGHT_UPPER_ANGLE
    MAX_UPRIGHT_LOWER_ANGLE = constants.BACK_MAX_UPRIGHT_LOWER_ANGLE

    MAX_LIFTUP_UPPER_ANGLE = constants.BACK_MAX_LIFTUP_UPPER_ANGLE
    MAX_LIFTUP_LOWER_ANGLE = constants.BACK_MAX_LIFTUP_LOWER_ANGLE


class LegSet:
    name = None
    LegFactory = None

    RIGHT_UPPER_PORT = None
    RIGHT_LOWER_PORT = None
    LEFT_UPPER_PORT = None
    LEFT_LOWER_PORT = None

    name = None
    right = None
    left = None

    def __init__(self):
        self.right = self.LegFactory(
            self.name+'-right', self.RIGHT_UPPER_PORT, self.RIGHT_LOWER_PORT)
        self.left = self.LegFactory(
            self.name+'-left', self.LEFT_UPPER_PORT, self.LEFT_LOWER_PORT)

    def connect(self):
        self.right.connect()
        self.left.connect()

    def disconnect(self):
        pass

    def reset(self):
        reset_grp = task.TaskGroup()
        reset_grp.add(self.right.reset)
        reset_grp.add(self.left.reset)
        reset_grp.start()
        reset_grp.join()

    def stand_up(self, pct, speed=constants.DEFAULT_SPEED, wait=True):
        if not (0.0 <= pct <= 100.0):
            raise ValueError('Value out of range: %d%%' % pct)
        reset_grp = task.TaskGroup()
        reset_grp.add(self.right.stand_up, (pct, speed))
        reset_grp.add(self.left.stand_up, (pct, speed))
        reset_grp.start()
        reset_grp.join()


class FrontLegSet(LegSet):
    name = 'front-legs'
    LegFactory = FrontLeg

    RIGHT_UPPER_PORT = constants.FRONT_RIGHT_LEG_UPPER_PORT
    RIGHT_LOWER_PORT = constants.FRONT_RIGHT_LEG_LOWER_PORT
    LEFT_UPPER_PORT = constants.FRONT_LEFT_LEG_UPPER_PORT
    LEFT_LOWER_PORT = constants.FRONT_LEFT_LEG_LOWER_PORT


class BackLegSet(LegSet):
    name = 'back-legs'
    LegFactory = BackLeg

    RIGHT_UPPER_PORT = constants.BACK_RIGHT_LEG_UPPER_PORT
    RIGHT_LOWER_PORT = constants.BACK_RIGHT_LEG_LOWER_PORT
    LEFT_UPPER_PORT = constants.BACK_LEFT_LEG_UPPER_PORT
    LEFT_LOWER_PORT = constants.BACK_LEFT_LEG_LOWER_PORT
