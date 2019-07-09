import asyncio
from signal import SIGINT, SIGTERM
import logging
from typing import List

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
