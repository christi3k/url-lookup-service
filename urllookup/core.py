import asyncio
from signal import SIGINT, SIGTERM
import logging
from urllookup.server_app import ServerApp
from urllookup.utils import signal_handler

logger = logging.getLogger(__package__)
logger.debug('core module loaded')

def main():
    """
    Here we create our ServerApp, set signals handlers, and manage main execution of event loop.
    """
    server_app: None = ServerApp()

    # get the current event loop
    loop = asyncio.get_event_loop()

    # turn on debugging TODO: Figure out where this goes
    loop.set_debug(True)

    # set up signals handling
    for sig in (SIGTERM, SIGINT):
        loop.add_signal_handler(sig, signal_handler, sig)

    # run event loop until our app server has completed startup
    loop.run_until_complete(server_app.start())

    # now run the event loop continuously
    # our ServerApp will run until the loop is stopped with SIGINT or SIGTERM
    loop.run_forever()

    # once the loop has been stopped with SIGINT or SIGTERM, the next running
    # of the loop is unblocked
    # next, we run the loop until stopping the app server is complete
    loop.run_until_complete(server_app.stop())

    # cancel currently pending tasks; this raises a CancelledError in each
    tasks = asyncio.Task.all_tasks()
    for t in tasks:
        t.cancel()

    # gather canceled tasks in a group and allow them to run until completion
    # (this allows CancelledError to be handled)
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)

    # finally, close the loop
    loop.close()
