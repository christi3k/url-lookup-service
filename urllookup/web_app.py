from aiohttp import web
import logging
from urllookup.route_handlers import RouteHandler

logger = logging.getLogger(__package__)

def get_app() -> web.Application:
    """
    Set up the web app that our AppRunner (ServerApp) will serve.

    TODO: Figure out if this should be blocking or not.
    """
    logger.debug('setting up app server')
    app = web.Application()

    router = app.router

    handler = RouteHandler()

    router.add_get('/', handler.handle)
    router.add_get('/{name}', handler.handle)

    return app
