
# -*- coding: utf-8 -*-

from enum import Enum
import logging
import coloredlogs

is_pi = False

if is_pi:
    from rpi_client.pololu.dual_mc33926_rpi import motors, MAX_SPEED
else:
    MAX_SPEED = 400

logger = logging.getLogger('rpi_server')
logger.propagate = False
log_config = {
    'level': 'DEBUG',
    'logger': logger,
    'milliseconds': True,
    'format': '%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s'
}
coloredlogs.install(**log_config)


class TurnDir(Enum):
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1


class CarState(object):

    def __init__(self):
        if is_pi:
            motors.enable()
            motors.setSpeeds(0, 0)
        self.stop()
        self.speed_inc = 10
        self.prev_state = (0, 0)

    def set_delta(self, val):
        if val < MAX_SPEED and val > -1 * MAX_SPEED:
            self.turn_delta = val

    def faster(self):
        self.left_speed += self.speed_inc
        self.right_speed += self.speed_inc

    def slower(self):
        self.left_speed -= self.speed_inc
        self.right_speed -= self.speed_inc

    def stop(self):
        self.left_speed = 0
        self.right_speed = 0
        self.turn_delta = 20
        self.turn_direction = TurnDir.STRAIGHT

    def in_bounds(self, item):
        if item < (-1 * MAX_SPEED):
            return -1 * MAX_SPEED
        elif item > MAX_SPEED:
            return MAX_SPEED
        return item

    def calc_speeds(self):
        calc_l = self.left_speed
        calc_r = self.right_speed
        if calc_l != 0 and calc_r != 0:
            if self.turn_direction == TurnDir.LEFT:
                calc_l -= self.turn_delta
                calc_r += self.turn_delta
            elif self.turn_direction == TurnDir.RIGHT:
                calc_l += self.turn_delta
                calc_r -= self.turn_delta
        calc_l = self.in_bounds(calc_l)
        calc_r = self.in_bounds(calc_r)
        return calc_l, calc_r

    def update_physical_state(self):
        calc_left_speed, calc_right_speed = self.calc_speeds()
        if (calc_left_speed, calc_right_speed) != self.prev_state:
            logger.info('New Speeds: L:  {} R:  {}'.format(calc_left_speed, calc_right_speed))
            if is_pi:
                motors.motor1.setSpeed(calc_left_speed)
                motors.motor2.setSpeed(calc_right_speed)
            self.prev_state = (calc_left_speed, calc_right_speed)
