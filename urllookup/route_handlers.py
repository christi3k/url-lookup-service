from aiohttp import web
from typing import Dict, Any
import logging

from urllookup.lookup import url_lookup

logger = logging.getLogger(__package__)

class RouteHandler:
    def __init__(self, redis_pool) -> None:
        self._redis_pool: Any = redis_pool

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
        url_info = await url_lookup(host_and_port=host_and_port, path_and_qs=path_and_qs, redis_pool=self._redis_pool)

        response: Dict = {}
        if url_info == None:
            response['status'] = 'NO INFO'
        elif url_info == b'ALLOW':
            response['status'] = 'ALLOWED'
        else:
            response['status'] = 'DISALLOWED'
        response['url_checked'] = {'host_and_port:': host_and_port, 'path_and_qs': path_and_qs}
        return web.json_response(response)
