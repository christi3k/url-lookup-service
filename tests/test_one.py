from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
import urllookup.core

class UrlLookupTestCase(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        app = urllookup.core.get_web_app()
        return app

    # the unittest_run_loop decorator can be used in tandem with
    # the AioHTTPTestCase to simplify running
    # tests that are asynchronous
    @unittest_run_loop
    async def test_anon(self):
        resp = await self.client.request("GET", "/")
        assert resp.status == 200
        text = await resp.text()
        assert "Hello, Anonymous" in text

    @unittest_run_loop
    async def test_christie(self):
        resp = await self.client.request("GET", "/Christie")
        assert resp.status == 200
        text = await resp.text()
        assert "Hello, Christie" in text
