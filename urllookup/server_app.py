import asyncio
from typing import Callable
from aiohttp import web
import logging
import urllookup.web_app as web_app

logger = logging.getLogger(__package__)

class ServerApp():
    """
    Class that generates the "Sever" app, which is an AppRunner for our main web app.
    """
    def __init__(self, host: str = '127.0.0.1', port: int = 9002) -> None:
        """
        Initialize properties we'll need later.

        TODO: parameterize host and port and possibly logging configuration.
        """
        self.loop = asyncio.get_event_loop()
        # self.app: Callable[[], web.Application] = web_app.get_app
        self.app: Callable[[], web.Application]
        self.runner: web.AppRunner
        self.host: str = host
        self.port: int = port 
        # set aithhtp access logging to package's (file) logger
        self.access_log: logging.Logger = logger

    async def start(self) -> None:
        """
        Start the application server and serve our web app.

        We'll do this first in the event loop, with run_until_complete().
        """
        app = await web_app.get_app()
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.host, self.port)
        logger.debug('Starting server on host: %s and port: %s', self.host, self.port)
        await site.start()

    async def stop(self) -> None:
        """
        Stop the application server and do required cleanup.

        We'll run this using run_until_complete() AFTER run_forever part of event loop completes.
        """
        await self.runner.cleanup()
