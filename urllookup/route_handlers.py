from aiohttp import web
import logging

from urllookup.lookup import url_lookup

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

    async def urlinfo(self, request: web.Request) -> web.Response:
        """
        Handle request for url info.
        """
        host_and_port: str = request.match_info.get('host_and_port')
        path_and_qs: str = request.match_info.get('path_and_qs')
        logger.debug('post and port: ' + host_and_port)
        logger.debug('path_and_qs: ' + path_and_qs)
        await url_lookup(host_and_port, path_and_qs)
        text: str = 'OK'
        return web.Response(text=text)
