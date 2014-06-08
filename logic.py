import logging
import threading
import gui

STACK = 1000

players = {}
players_lock = threading.RLock()


class Player:
    def __init__(self, transport, username):
        self.net_transport = transport
        self.username = username
        self.widget = gui.window.take_a_seat(username, STACK)
        players[username] = self
        self.messages = []

    def incoming_message(self, message):
        logging.debug("Message:{}".format(message))
        with players_lock:
            self.messages.append(message)

    def get_message(self):
        with players_lock:
            return self.messages.pop(0)

    def disconnect(self):
        pass