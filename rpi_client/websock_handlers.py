# -*- coding: utf-8 -*-

from tornado.websocket import WebSocketHandler
import json
from rpi_client.car_state import TurnDir


class DriverSocketHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        self.application.log.info('New websocket!')
        pass

    def on_message(self, message):
        self.application.log.info('Received message: {}'.format(message))
        parsed_msg = json.loads(message)
        if 'message' not in parsed_msg:
            self.application.log.info("Invalid message received: {}".format(message))
            return None
        action = parsed_msg['message']
        if action == 'stop':
            self.application.car_state.stop()
        elif action == 'faster':
            self.application.car_state.faster()
        elif action == 'slower':
            self.application.car_state.slower()
        elif action == 'right':
            self.application.car_state.turn_direction = TurnDir.RIGHT
        elif action == 'left':
            self.application.car_state.turn_direction = TurnDir.LEFT
        elif action == 'straight':
            self.application.car_state.turn_direction = TurnDir.STRAIGHT

    def on_close(self):
        pass
