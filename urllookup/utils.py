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
        ('mozilla.org:80/index.html','ALLOW'),
        ('mozilla.org:443/index.html','ALLOW'),
        ('mazilla.org:80/actuallybad.html?areyousure=yes', 'DISALLOW'),
        ('phishing4ever:443/index.html', 'DISALLOW'),
        ('capital0ne.ru:8080/download.html', 'DISALLOW'),
        ('capitalone.com:443','ALLOW'),
        ('capitalone.com:443/index.html','ALLOW'),
        ('goodsite.com:80/index.html?newuser=yes','ALLOW'),
        ('goodsite.com:443/sites/index.html', 'ALLOW'),
        ('washingtonpost.com:443/index.html', 'ALLOW'),
        ('washingt0np0st.com:8080/nope.html', 'DISALLOW'),
        ('not.actually.ebay.badsites.us:80/index.html', 'DISALLOW'),
    ]
    return test_urls

def load_config():
    # parse command-line arguments and set config list
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", dest="host", default="127.0.0.1", help="address to listen on")
    parser.add_argument("--port", dest="port", default="9001", help="port to listen on")
    parser.add_argument("--redis-host", dest="redis_host", default="127.0.0.1", help="host for redis instance")
    parser.add_argument("--redis-port", dest="redis_port", default="6379", help="port for redis instance")
    parser.add_argument("--redis-min", dest="redis_min", default=1, help="min size for redis pool")
    parser.add_argument("--redis-max", dest="redis_max", default=5, help="max size for redis pool")
    config: Dict = vars(parser.parse_args())
    return config


