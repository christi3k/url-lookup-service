import json
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from typing import Dict
import urllookup.core

class End2EndRedisTestCase(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        config: Dict = {'host': '127.0.0.1', 'port': '9001', 'redis_host': '127.0.0.1', 'redis_port': '6379', 'redis_min': 1, 'redis_max': 5, 'no_redis': False}
        app = await urllookup.web_app.get_app(config)
        return app

    @unittest_run_loop
    async def test_urlinfo_disallowed(self):
        # try a DISALLOWED URL
        response = await self.client.request("GET", '/urlinfo/1/cnn.com%3A443/badstuff.html%3Fgivemeit%3Dyes')
        assert response.status == 200
        assert 'application/json' == response.content_type
        text = await response.text()
        expected = json.dumps({"status": "DISALLOWED", "url_checked": {"host_and_port:": "cnn.com:443", "path_and_qs": "badstuff.html?givemeit=yes"}})
        assert text == expected

    @unittest_run_loop
    async def test_urlinfo_allowed(self):
        # try an ALLOWED url
        response = await self.client.request("GET", '/urlinfo/1/mozilla.org%3A80/index.html')
        assert response.status == 200
        assert 'application/json' == response.content_type
        text = await response.text()
        expected = json.dumps({"status": "ALLOWED", "url_checked": {"host_and_port:": "mozilla.org:80", "path_and_qs": "index.html"}})
        assert text == expected

    @unittest_run_loop
    async def test_urlinfo_noinfo(self):
        # try a url not in the database
        response = await self.client.request("GET", '/urlinfo/1/debian.org%3A80/index.html')
        assert response.status == 200
        assert 'application/json' == response.content_type
        text = await response.text()
        expected = json.dumps({"status": "NO INFO", "url_checked": {"host_and_port:": "debian.org:80", "path_and_qs": "index.html"}})
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

class End2EndLocalTestCase(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        config: Dict = {'host': '127.0.0.1', 'port': '9001', 'redis_host': '127.0.0.1', 'redis_port': '6379', 'redis_min': 1, 'redis_max': 5, 'no_redis': True}
        app = await urllookup.web_app.get_app(config)
        return app

    @unittest_run_loop
    async def test_urlinfo_disallowed(self):
        # try a DISALLOWED URL
        response = await self.client.request("GET", '/urlinfo/1/cnn.com%3A443/badstuff.html%3Fgivemeit%3Dyes')
        assert response.status == 200
        assert 'application/json' == response.content_type
        text = await response.text()
        expected = json.dumps({"status": "DISALLOWED", "url_checked": {"host_and_port:": "cnn.com:443", "path_and_qs": "badstuff.html?givemeit=yes"}})
        assert text == expected

    @unittest_run_loop
    async def test_urlinfo_allowed(self):
        # try an ALLOWED url
        response = await self.client.request("GET", '/urlinfo/1/mozilla.org%3A80/index.html')
        assert response.status == 200
        assert 'application/json' == response.content_type
        text = await response.text()
        expected = json.dumps({"status": "ALLOWED", "url_checked": {"host_and_port:": "mozilla.org:80", "path_and_qs": "index.html"}})
        assert text == expected

    @unittest_run_loop
    async def test_urlinfo_noinfo(self):
        # try a url not in the database
        response = await self.client.request("GET", '/urlinfo/1/debian.org%3A80/index.html')
        assert response.status == 200
        assert 'application/json' == response.content_type
        text = await response.text()
        expected = json.dumps({"status": "NO INFO", "url_checked": {"host_and_port:": "debian.org:80", "path_and_qs": "index.html"}})
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
