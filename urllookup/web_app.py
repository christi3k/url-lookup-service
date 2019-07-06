from aiohttp import web
import logging
from urllookup.route_handlers import RouteHandler

logger = logging.getLogger(__package__)

async def get_app() -> web.Application:
    """
    Set up the web app that our AppRunner (ServerApp) will serve.

    TODO: Figure out if this should be blocking or not.
    """
    logger.debug('setting up app server')
    app = web.Application()

    router = app.router

    handler = RouteHandler()

    # router.add_get('/', handler.handle)
    # router.add_get('/{name}', handler.handle)

    router.add_get('/urlinfo/1/{host_and_port}/{path_and_qs}', handler.urlinfo, name='check')

    return app
