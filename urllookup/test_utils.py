# test_utils.py
#
# This module contains functions that help with testing of asynchronous
# methods. Most of this code originates from the aiohttp library. I extracted
# just what was needed to test asynchrounous methods WITHOUT requiring
# instances from the aiohttp library such as an application.

import asyncio
import contextlib
import functools
import gc
import sys
from typing import Callable, Any

def unittest_run_loop(func: Any, *args: Any, **kwargs: Any) -> Any:
    """A decorator dedicated to use with asynchronous methods of
    unittest.TestCase.
    """

    @functools.wraps(func, *args, **kwargs)
    def new_func(self: Any, *inner_args: Any, **inner_kwargs: Any) -> Any:
        return self.loop.run_until_complete(
            func(self, *inner_args, **inner_kwargs))

    return new_func

_LOOP_FACTORY = Callable[[], asyncio.AbstractEventLoop]

def setup_test_loop(
        loop_factory: _LOOP_FACTORY=asyncio.new_event_loop
) -> asyncio.AbstractEventLoop:
    """Create and return an asyncio.BaseEventLoop
    instance.
    The caller should also call teardown_test_loop,
    once they are done with the loop.
    """
    loop = loop_factory()
    try:
        module = loop.__class__.__module__
        skip_watcher = 'uvloop' in module
    except AttributeError:  # pragma: no cover
        # Just in case
        skip_watcher = True
    asyncio.set_event_loop(loop)
    if sys.platform != "win32" and not skip_watcher:
        policy = asyncio.get_event_loop_policy()
        watcher = asyncio.SafeChildWatcher()  # type: ignore
        watcher.attach_loop(loop)
        with contextlib.suppress(NotImplementedError):
            policy.set_child_watcher(watcher)
    return loop

def teardown_test_loop(loop: asyncio.AbstractEventLoop,
                       fast: bool=False) -> None:
    """Teardown and cleanup an event_loop created
    by setup_test_loop.
    """
    closed = loop.is_closed()
    if not closed:
        loop.call_soon(loop.stop)
        loop.run_forever()
        loop.close()

    if not fast:
        gc.collect()

    asyncio.set_event_loop(None)
