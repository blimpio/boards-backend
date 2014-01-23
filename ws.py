import os
import json

from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection

# Set Django Environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'blimp.settings'

from blimp.utils.websockets import WebSocketRequest


class RESTAPIConnection(SockJSConnection):
    def on_open(self, info):
        self.send_json({'connected': True})

    def on_message(self, data):
        response = WebSocketRequest(data).get_response()
        self.send_json(response)

    def send_json(self, obj):
        self.send(json.dumps(obj))


if __name__ == '__main__':
    import logging
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--port',
        help='Optional port number. Defaults to 8080',
        default=8080,
    )
    parser.add_argument(
        '--debug',
        help='Verbosity level set to DEBUG. Defaults to WARNING.',
        action='store_const',
        dest='loglevel',
        const=logging.DEBUG,
        default=logging.WARNING
    )
    parser.add_argument(
        '--verbose',
        help='Verbosity level set to INFO.',
        action='store_const',
        dest='loglevel',
        const=logging.INFO
    )

    args = parser.parse_args()
    port = args.port

    logging.getLogger().setLevel(args.loglevel)

    EchoRouter = SockJSRouter(RESTAPIConnection, '/ws/api/')

    app = web.Application(EchoRouter.urls)
    app.listen(port)

    logging.info(" [*] Listening on 0.0.0.0:{}".format(port))

    ioloop.IOLoop.instance().start()
