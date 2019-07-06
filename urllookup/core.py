import asyncio
from signal import SIGINT, SIGTERM
import logging
from typing import Callable
from aiohttp import web

logger = logging.getLogger(__package__)
logger.debug('core module loaded')

async def handle(request: web.Request) -> web.Response:
    """
    Generic handler for a request, just to get us going.
    """
    name: str = request.match_info.get('name', "Anonymous")
    logger.debug('Name: ' + name)
    text: str = "Hello, " + name
    return web.Response(text=text)

def get_web_app() -> web.Application:
    """
    Set up the web app that our AppRunner (ServerApp) will serve.

    TODO: Figure out if this should be blocking or not.
    """
    logger.debug('setting up app server')
    app = web.Application()

    router = app.router

    router.add_get('/', handle)
    router.add_get('/{name}', handle)

    return app

class ServerApp:
    """
    Class that generates the "Sever" app, which is an AppRunner for our main web app.
    """
    def __init__(self) -> None:
        """
        Initialize properties we'll need later.

        TODO: parameterize host and port and possibly logging configuration.
        """
        self.loop = asyncio.get_event_loop()
        self.app: Callable[[], web.Application] = get_web_app
        self.runner: web.AppRunner
        self.host: str = '127.0.0.1'
        self.port: int = 9002
        # set aithhtp access logging to package's (file) logger
        self.access_log: logging.Logger = logger

    async def start(self) -> None:
        """
        Start the application server and serve our web app.

        We'll do this first in the event loop, with run_until_complete().
        """
        self.runner = web.AppRunner(self.app())
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()

    async def stop(self) -> None:
        """
        Stop the application server and do required cleanup.

        We'll run this using run_until_complete() AFTER run_forever part of event loop completes.
        """
        await self.runner.cleanup()

def signal_handler(sig) -> None:
    """
    Stop the event look upon SIGINT and SIGTERM.

    Remove handlers afterwards so program can continue gracefully shutting down.
    """
    loop = asyncio.get_event_loop()
    loop.stop()
    print(f'Got signal: {sig!s}, shutting down.')
    loop.remove_signal_handler(SIGTERM)
    loop.add_signal_handler(SIGINT, lambda: None)

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
