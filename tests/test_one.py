import json
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
import urllookup.core

class UrlLookupTestCase(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        app = await urllookup.web_app.get_app()
        return app

    # the unittest_run_loop decorator can be used in tandem with
    # the AioHTTPTestCase to simplify running
    # tests that are asynchronous
    # @unittest_run_loop
    # async def test_anon(self):
        # resp = await self.client.request("GET", "/")
        # assert resp.status == 200
        # text = await resp.text()
        # assert "Hello, Anonymous" in text

    # @unittest_run_loop
    # async def test_christie(self):
        # resp = await self.client.request("GET", "/Christie")
        # assert resp.status == 200
        # text = await resp.text()
        # assert "Hello, Christie" in text

    @unittest_run_loop
    async def test_urlinfo(self):
        response = await self.client.request("GET", '/urlinfo/1/cnn.com%3A443/badstuff.html%3Fgivemeit%3Dyes')
        assert response.status == 200
        assert 'application/json' == response.content_type
        text = await response.text()
        expected = json.dumps({"status": "OK", "url_checked": {"host_and_port:": "cnn.com:443", "path_and_qs": "badstuff.html?givemeit=yes"}})
        assert text == expected
