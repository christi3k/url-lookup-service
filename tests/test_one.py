import json
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from typing import Dict
import urllookup.core

class UrlLookupTestCase(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        config: Dict = {'host': '127.0.0.1', 'port': '9001', 'redis_host': '127.0.0.1', 'redis_port': '6379', 'redis_min': 1, 'redis_max': 5}
        app = await urllookup.web_app.get_app(config)
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

# redis_pool.get(url_to_lookup)

    @unittest_run_loop
    async def test_urlinfo(self):
        response = await self.client.request("GET", '/urlinfo/1/cnn.com%3A443/badstuff.html%3Fgivemeit%3Dyes')
        assert response.status == 200
        assert 'application/json' == response.content_type
        text = await response.text()
        expected = json.dumps({"status": "DISALLOWED", "url_checked": {"host_and_port:": "cnn.com:443", "path_and_qs": "badstuff.html?givemeit=yes"}})
        assert text == expected

    @unittest_run_loop
    async def test_catchall(self):
        # test with single-level path
        response = await self.client.request("GET", '/badurl')
        assert response.status == 404
        text = await response.text()
        assert text == 'YOU GOT A 404!'

        response = await self.client.request("GET", '/badurl/one/two/three')
        assert response.status == 404
        text = await response.text()
        assert text == 'YOU GOT A 404!'
