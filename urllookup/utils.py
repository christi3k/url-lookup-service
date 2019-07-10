import asyncio
from signal import SIGINT, SIGTERM
import logging
import argparse
from typing import List, Dict

logger = logging.getLogger(__package__)

def signal_handler(sig) -> None:
    """
    Stop the event look upon SIGINT and SIGTERM.

    Remove handlers afterwards so program can continue gracefully shutting down.
    """
    loop = asyncio.get_event_loop()
    loop.stop()
    print(f'Got signal: {sig!s}, shutting down.')
    loop.remove_signal_handler(SIGTERM)
    loop.add_signal_handler(SIGINT, lambda: None)

def get_test_urls() -> List:
    test_urls: List = [
        ('mozilla.org:80/index.html',b'ALLOW'),
        ('mozilla.org:443/index.html',b'ALLOW'),
        ('mazilla.org:80/actuallybad.html?areyousure=yes', b'DISALLOW'),
        ('phishing4ever:443/index.html', b'DISALLOW'),
        ('capital0ne.ru:8080/download.html', b'DISALLOW'),
        ('capitalone.com:443',b'ALLOW'),
        ('capitalone.com:443/index.html',b'ALLOW'),
        ('nestedsite.com:443/one/two/three/index.html',b'ALLOW'),
        ('goodsite.com:80/index.html?newuser=yes',b'ALLOW'),
        ('goodsite.com:443/sites/index.html', b'ALLOW'),
        ('washingtonpost.com:443/index.html', b'ALLOW'),
        ('washingt0np0st.com:8080/nope.html', b'DISALLOW'),
        ('not.actually.ebay.badsites.us:80/index.html', b'DISALLOW'),
        ('cnn.com:443/badstuff.html?givemeit=yes', b'DISALLOW'),
    ]
    return test_urls

def load_config():
    # parse command-line arguments and set config list
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", dest="host", default="127.0.0.1", help="address to listen on. default: 127.0.0.1")
    parser.add_argument("--port", dest="port", default="9001", help="port to listen on. default: 9001")
    parser.add_argument("--redis-host", dest="redis_host", default="127.0.0.1", help="host for redis instance. default: 127.0.0.1")
    parser.add_argument("--redis-port", dest="redis_port", default="6379", help="port for redis instance. default: 6379")
    parser.add_argument("--redis-min", dest="redis_min", default=1, help="min size for redis pool. default: 1")
    parser.add_argument("--redis-max", dest="redis_max", default=5, help="max size for redis pool. default: 5")
    parser.add_argument("--no-redis", dest="no_redis", default=False, help="use local lookup instead of redis")
    config: Dict = vars(parser.parse_args())
    return config


