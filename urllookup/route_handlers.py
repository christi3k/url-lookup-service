from aiohttp import web
import logging

logger = logging.getLogger(__package__)

class RouteHandler:
    def __init__(self) -> None:
        pass

    async def handle(self, request: web.Request) -> web.Response:
        """
        Generic handler for a request, just to get us going.
        """
        name: str = request.match_info.get('name', "Anonymous")
        logger.debug('Name: ' + name)
        text: str = "Hello, " + name
        return web.Response(text=text)
