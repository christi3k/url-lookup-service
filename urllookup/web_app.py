import asyncio
from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher
import aioredis
import logging
from typing import Dict
from urllookup.route_handlers import RouteHandler

logger = logging.getLogger(__package__)

async def get_app(config: Dict) -> web.Application:
    """
    Set up the web app that our AppRunner (ServerApp) will serve.

    Includes initializing redis coonection pool.

    TODO: Encapsulate conf and make it user settable.
    """
    logger.debug('setting up app server')
    app = web.Application()

    router = app.router

    handler = RouteHandler()

    conf = {'host': config['redis_host'],
            'port': config['redis_port'],
            'minsize': config['redis_min'],
            'maxsize': config['redis_max']}

    redis_pool = await setup_redis(app, conf)
    handler.set_processor(redis_pool)
    await set_routes(router, handler)

    return app

async def set_routes(router: UrlDispatcher, handler: RouteHandler) -> None:
    """
    Attach all routes (urls) to handlers.
    """
    router.add_get('/urlinfo/1/{host_and_port}/{path_and_qs}', handler.urlinfo, name='check')
    router.add_get('/{tail:.*}', handler.catchall)
    return

async def setup_redis(app, conf) -> None:
    """
    Set up redis pool.

    Includes appending the closing of redis to app's on_cleanup.
    """
    loop = asyncio.get_event_loop()
    pool = await aioredis.create_redis_pool(
        (conf['host'], conf['port']),
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=loop
    )

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    return pool
