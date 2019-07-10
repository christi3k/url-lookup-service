import unittest
from unittest.mock import patch
import json

from urllookup.test_utils import unittest_run_loop, setup_test_loop, teardown_test_loop
import urllookup.route_handlers


class RouteHandlerTestCase(unittest.TestCase):
    """
    Test case for RouteHandler methods.

    Each test method in this class will likely need to have the
    @unittest_run_loop decorator. These tests also make use of the mock.patch
    decorator in order to mock the web.Request object that is passed to each route
    handler.

    Use the `return_value` property to explicitly set the return value of a
    mocked method. Use the side_effect property when return values for the
    web.Request methods (e.g. get) need to return values dependent on their
    input.
    """

    def setUp(self) -> None:
        """
        Set up event loop and initialize RouteHandler class.
        """
        self.loop = setup_test_loop()
        self.handler = urllookup.route_handlers.RouteHandler(redis_pool=None)

    @unittest_run_loop
    @patch('urllookup.route_handlers.web.Request', autospec=True)
    async def test_catchall(self, mock_webrequest):
        """
        RouteHandler.catchall returns a 404 for all urls that don't already
        have handlers attached. 

        It's not necessary to mock any return_values because it returns a 404
        Not Found regardless of input.
        """
        response = await self.handler.catchall(mock_webrequest)
        self.assertEqual(response.status, 404)
        self.assertEqual(response.text, 'YOU GOT A 404!')
        self.assertEqual(response.reason, 'Not Found')

    @unittest_run_loop
    @patch('urllookup.route_handlers.web.Request', autospec=True)
    async def test_urlinfo(self, mock_webrequest):
        """
        RouteHandler.urlinfo() looks up the given url and returns information about it. 

        It always returns 200 OK regardless of input. However, the response
        text differs based on input, so we need to set a function-based
        side_effect.
        """
       
        # test an ALLOWED url
        side_effect = lambda x: {'host_and_port': 'mozilla.org:80', 'path_and_qs': 'index.html'}[x]
        mock_webrequest.match_info.get.side_effect = side_effect

        response = await self.handler.urlinfo(mock_webrequest)
        self.assertEqual(response.status, 200)
        expected_text = json.dumps({"status": "ALLOWED", "url_checked": {"host_and_port:": "mozilla.org:80", "path_and_qs": "index.html"}})
        self.assertEqual(response.text, expected_text)
        self.assertEqual(response.reason, 'OK')

        # test a DISALLOWED url
        side_effect = lambda x: {'host_and_port': 'cnn.com:443', 'path_and_qs': 'badstuff.html?givemeit=yes'}[x]
        mock_webrequest.match_info.get.side_effect = side_effect

        response = await self.handler.urlinfo(mock_webrequest)
        self.assertEqual(response.status, 200)
        expected_text = json.dumps({"status": "DISALLOWED", "url_checked": {"host_and_port:": "cnn.com:443", "path_and_qs": "badstuff.html?givemeit=yes"}})
        self.assertEqual(response.text, expected_text)
        self.assertEqual(response.reason, 'OK')

        # test a url not in database (NO INFO)
        side_effect = lambda x: {'host_and_port': 'debian.org:80', 'path_and_qs': 'index.html'}[x]
        mock_webrequest.match_info.get.side_effect = side_effect

        response = await self.handler.urlinfo(mock_webrequest)
        self.assertEqual(response.status, 200)
        expected_text = json.dumps({"status": "NO INFO", "url_checked": {"host_and_port:": "debian.org:80", "path_and_qs": "index.html"}})
        self.assertEqual(response.text, expected_text)
        self.assertEqual(response.reason, 'OK')

    def tearDown(self) -> None:
        """
        Stop and clean up event loop.
        """
        teardown_test_loop(self.loop)
