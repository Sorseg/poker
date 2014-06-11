import asyncio
import json
import logging
import logic

PORT = 12321
loop = asyncio.get_event_loop()

messages = asyncio.Queue()


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
                self.transport.write('{"ERROR": "username please"}')
                return
            self.player = logic.Player(self, username)
            # TODO: broadcast

        self.player.incoming_message(message)

    def connection_lost(self, exc):
        logging.debug("Disconnected:{}".format(self.peer))
        self.player.disconnect()


def create_server():
    @asyncio.coroutine
    def coroutine():
        logging.debug("Making server...")
        srv = yield from loop.create_server(Server, '0.0.0.0', PORT)
        logging.debug("Hosted server:{!r}".format(srv))
        return srv

    loop.call_soon_threadsafe(asyncio.Task, coroutine())


def stop():
    loop.call_soon_threadsafe(loop.stop)


def create_client(username, host):
    class Client(asyncio.Protocol):
        def connection_made(self, transport):
            self.transport = transport
            logging.debug("Connection made")
            self.send_message({'username': username})

        def send_message(self, msg):
            self.transport.write(json.dumps(msg).encode())

        def data_received(self, data):
            messages.put_nowait(json.loads(data))

    @asyncio.coroutine
    def connect_coroutine(address, port):
        conn = yield from loop.create_connection(Client, address, port)
        logging.info("Connected! {}".format(conn))

    loop.call_soon_threadsafe(asyncio.Task, connect_coroutine(host, PORT))
