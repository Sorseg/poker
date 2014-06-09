import logging
logging.basicConfig(level=logging.DEBUG)
import gui
import async
import threading


threading.Thread(target=gui.main, name="Main GUI thread").start()
async.loop.run_forever()

