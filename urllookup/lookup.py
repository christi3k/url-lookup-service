import aioredis
from typing import Any, Union
import logging
from urllookup.utils import get_test_urls

logger = logging.getLogger(__package__)

async def url_lookup(host_and_port: str, path_and_qs: str, redis_pool: Any) -> Union[bytes, None]:
    url_to_lookup = host_and_port + '/' + path_and_qs
    if isinstance(redis_pool, aioredis.commands.Redis):
        info = await redis_pool.get(url_to_lookup)
    else:
        info = await local_lookup(url_to_lookup)
    return info

async def local_lookup(url_to_lookup: str) -> Union[bytes, None]:
    test_urls = dict(get_test_urls())
    if url_to_lookup in test_urls:
        return test_urls[url_to_lookup]
    else:
        return None



