import logging
import json

from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection

from blimp.utils.websockets import WebSocketsRequest


class EchoConnection(SockJSConnection):
    def on_open(self, info):
        self.send_json({'connected': True})

    def on_message(self, data):
        response = WebSocketsRequest(data).get_response()
        self.send_json(response)

    def send_json(self, obj):
        self.send(json.dumps(obj))

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)

    EchoRouter = SockJSRouter(EchoConnection, '/echo')

    app = web.Application(EchoRouter.urls)
    app.listen(8080)

    logging.info(" [*] Listening on 0.0.0.0:8080")

    ioloop.IOLoop.instance().start()
