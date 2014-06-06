import asyncio
import concurrent.futures
import json
import logging
import logic

PORT = 12321
loop = asyncio.get_event_loop()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


class Server(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.peer = transport.get_extra_info('peername')
        logging.debug("Connected:{}".format(self.peer))
        self.player = None

    def data_received(self, data):
        message = json.loads(data.decode('utf8'))
        if not self.player:
            username = message.get('username', None)
            if not username:
                logging.error("No username from {}".format(self.peer))
                self.transport.write("ERROR:username please")
                return
            self.player = logic.Player(self, username)
            # TODO: broadcast

        self.player.incoming_message(message)

    def connection_lost(self, exc):
        logging.debug("Disconnected:{}".format(self.peer))
        self.player.disconnect()


@asyncio.coroutine
def coroutine_create_server():
    logging.debug("Making server...")
    srv = yield from loop.create_server(Server, '0.0.0.0', PORT)
    logging.debug("Hosted server:{!r}".format(srv))
    return srv


def create_server():
    loop.call_soon_threadsafe(asyncio.Task,
                              coroutine_create_server())


def run(app):
    loop.run_in_executor(executor, app)
    loop.run_forever()


def stop():
    loop.call_soon_threadsafe(loop.stop)


class Client(asyncio.Protocol):
    def connection_made(self, transport):
        logging.debug("Connection made")



