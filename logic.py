import threading
import gui

players = {}
players_lock = threading.RLock()


class Player:
    def __init__(self, transport, username):
        self.net_transport = transport
        self.username = username
        self.widget = gui.window.take_a_seat()
        players[username] = self
        self.messages = []

    def incoming_message(self, message):
        with players_lock:
            self.messages.append(message)

    def get_message(self):
        with players_lock:
            return self.messages.pop(0)

    def disconnect(self):
        pass