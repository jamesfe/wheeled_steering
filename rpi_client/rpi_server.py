# -*- coding: utf-8 -*-
"""The main entry point for our little car. """

import logging
import sys

import coloredlogs
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application

from rpi_client.http_handlers import MainHandler
from rpi_client.car_state import CarState
from rpi_client.websock_handlers import DriverSocketHandler

logger = logging.getLogger('rpi_server')
logger.propagate = False
log_config = {
    'level': 'DEBUG',
    'logger': logger,
    'milliseconds': True,
    'format': '%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s'
}
coloredlogs.install(**log_config)


class CarServer(Application):

    def __init__(self, ioloop=None):
        urls = [
            (r'/', MainHandler),
            (r'/control_socket', DriverSocketHandler)
        ]
        self.car_state = CarState()
        self.log = logger
        super(CarServer, self).__init__(urls, debug=True, autoreload=False)


def main():
    app = CarServer()

    try:
        logger.info('Opening HTTP server.')
        http_server = HTTPServer(app)
        # http_server.listen(9001, address='127.0.0.1')
        http_server.listen(9001, address='192.168.1.37')
        update_ms = 100
        logger.debug('Registering periodic callback. Every {} ms'.format(update_ms))
        i = PeriodicCallback(app.car_state.update_physical_state, update_ms)
        i.start()
        IOLoop.current().start()
    except (SystemExit, KeyboardInterrupt):
        pass

    logger.info('Stopping server.')
    http_server.stop()

    IOLoop.current().stop()
    sys.exit(0)


if __name__ == '__main__':
    main()
