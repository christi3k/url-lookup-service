import asyncio
from random import randint
import logging

logger = logging.getLogger(__package__)

async def url_lookup(host_and_port: str, path_and_qs: str) -> bool:
    logger.debug('looking up url...')
    wait = randint(0,4)
    await asyncio.sleep(wait)
    logger.debug('done looging up url...')
    return True
