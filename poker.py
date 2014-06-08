import logging
import gui
import async
import threading
logging.basicConfig(level=logging.DEBUG)

threading.Thread(target=gui.main, name="Main GUI thread").start()
async.loop.run_forever()

