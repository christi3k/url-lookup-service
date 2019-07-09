import asyncio
from random import randint
import logging

logger = logging.getLogger(__package__)

async def url_lookup(redis_pool, host_and_port: str, path_and_qs: str) -> bool:
    url_to_lookup = host_and_port + '/' + path_and_qs
    info = await redis_pool.get(url_to_lookup)
    if info == b'ALLOW':
        return True
    else:
        return False
