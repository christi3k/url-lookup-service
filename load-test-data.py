import asyncio
import aioredis
from urllookup.utils import get_test_urls

async def main():
    """
    Load redis with some test url data.
    """
    test_urls = get_test_urls()
    conf = {'host':'127.0.0.1', 'port': 6379, 'minsize':1, 'maxsize':5}
    loop = asyncio.get_event_loop()

    pool = await aioredis.create_redis_pool(
        (conf['host'], conf['port']),
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=loop
    )

    for url in test_urls:
        await pool.set(url[0], url[1])
    pool.close()
    await pool.wait_closed()    # closing all open connections

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
