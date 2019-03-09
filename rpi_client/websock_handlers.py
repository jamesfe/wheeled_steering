# -*- coding: utf-8 -*-

from tornado.websocket import WebSocketHandler


class DriverSocketHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        self.application.log.info('New websocket!')
        pass

    def on_message(self, message):
        self.application.log.info('Received message')
        self.application.log.info(message)

    def on_close(self):
        pass
