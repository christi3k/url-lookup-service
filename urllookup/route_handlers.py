from aiohttp import web
from typing import Dict, Any
import logging

from urllookup.lookup import url_lookup

logger = logging.getLogger(__package__)

class RouteHandler:
    def __init__(self) -> None:
        self._redis_pool: Any = None

    async def handle(self, request: web.Request) -> web.Response:
        """
        Generic handler for a request, just to get us going.
        """
        name: str = request.match_info.get('name', "Anonymous")
        logger.debug('Name: ' + name)
        text: str = "Hello, " + name
        return web.Response(text=text)

    async def catchall(self, request: web.Request) -> web.Response:
        """
        Handler for all routes not otherwise mapped.
        """
        return web.Response(status=404, text='YOU GOT A 404!')

    async def urlinfo(self, request: web.Request) -> web.Response:
        """
        Handle request for url info.
        """
        host_and_port: str = request.match_info.get('host_and_port')
        path_and_qs: str = request.match_info.get('path_and_qs')
        logger.debug('host and port: ' + host_and_port)
        logger.debug('path_and_qs: ' + path_and_qs)
        url_info = await url_lookup(self._redis_pool, host_and_port, path_and_qs)
        response: Dict = {}
        if(url_info):
            response['status'] = 'ALLOWED'
        else:
            response['status'] = 'DISALLOWED'
        response['url_checked'] = {'host_and_port:': host_and_port, 'path_and_qs': path_and_qs}
        return web.json_response(response)

    def set_processor(self, redis_pool):
        self._redis_pool = redis_pool
