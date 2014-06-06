import logging
import gui
import async
logging.basicConfig(level=logging.DEBUG)


async.loop.run_in_executor(async.executor, gui.main)
async.loop.run_forever()

