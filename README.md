## About

This project is a proof-of-concept exercise to demonstrate a highly available URL lookup service using Python. It utilizes asynio, aiohttp, and aioredis.

Clients request URL information via GET requests to a URL of the form: 

```
/urlinfo/1/{host_and_port}/{path_and_qs}
```

For the purposes of this exercise, http and https URLs are considered the same.

## Installation

### Prerequisites

- Python 3.7 environment. Using something like virtualenv highly recommended.
- MacOS or Linux-based OS. (Tested on macOS Mojave 10.14.5 and Ubuntu 18.04.)
- Git client.
- Terminal client.

### Install urllookup

1. Open a terminal window and clone the repository and change into it:

```
$ git clone https://github.com/christi3k/url-lookup-service.git
...
$ cd url-lookup-service
```

2. (Optional) Set up your python virtual environment. If you're not using a virtual environment, skip this step. 

Here's how you set up the environment using virtualenv:

```
$ virtualenv .venv -p python3
...
$ source .venv/bin/activate
```

Once the vitualenv is activated, you should see `(.venv)` prefixed to your prompt. You only need to _create_ the virtualenv once, but typically you'll need to activate it each time you're working in a new shell.

3. Install required modules via pip:

```
$ pip install -r requirements.txt
```

**(Optional) Docker installation**

If you wish to use the supplied `docker_compose.yml` for running a test Redis instance, you'll need to have Docker installed.

On macOS, you'll want [Docker Desktop](https://download.docker.com/mac/stable/Docker.dmg). Instructions for installing docker on Linux vary. Here are instructions for [Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04).

## Usage

### Starting redis via docker (optional)

If you'd like to use Docker to run a local redis instance, run:

```
$ docker-compose -f docker-compose.yml up -d redis
```

And if you'd like to interact with the Redis instance (e.g. to read or write test data), you can do so with:

```
$ docker exec -it container-name redis-cli
```

(Get the name of the running container with `docker ps`.)

If you elect to use the local redis instance, you'll probably some some test data to work with:

```
$ python load-test-data.py
```

This will load the urls from `urllookup/utils.py:get_test_urls()` into the running redis instance. This same url list is what is used for the fallback, local lookup service.

### Starting urllookup service

To start the urllookup service:

```
$ python run.py
```

This will start the url-lookup service on the default host of `127.0.0.1` and port `9001`. The service is also configured by default to query a Redis cluster for url information at `127.0.0.1` and port `6379` with a min pool size of 1 and max of 5.

Each of these values can be overridden via the command line. Use `python run.py --help` to see help documentation.

To run the urllookup service without a redis cluster, use:

```
$ python run.py --no-redis true
```

Note: If urllookup cannot connect to redis upon starting up, it will fallback to using the local lookup option.

### Checking urls

While the server is running, you can try out the service using your browser or another http client such as `curl`.

There are a handful of allowed and disallowed urls that come preloaded with this proof of concept.

Here's a `curl` call for a disallowed url:
```
curl http://127.0.0.1:9001/urlinfo/1/cnn.com%3A443/badstuff.html%3Fgivemeit%3Dyes

{"status": "DISALLOWED", "url_checked": {"host_and_port:": "cnn.com:443", "path_and_qs": "badstuff.html?givemeit=yes"}}
```

And one for an allowed url:
```
curl http://127.0.0.1:9001/urlinfo/1/mozilla.org%3A80/index.html

{"status": "ALLOWED", "url_checked": {"host_and_port:": "mozilla.org:80", "path_and_qs": "index.html"}}
```
### Request format

Per the supplied requirements, this API proof-of-concept requires the following request format:

```
GET /urlinfo/1/{host_and_port}/{path_and_qs}
```

**_Both_ parameters must be url-encoded:**

- `{host_and_port}` host and port of the destination url.
- `{path_and_qs}`: path and query sting of the destination url.

`path_and_qs` should not have a leading forward-slash. Nested paths are permissible when url-encoded.

Correct:

```
http://127.0.0.1:9001/urlinfo/1/nestedsite.com%3A443/one%2Ftwo%2Fthree%2Findex.html
```

Incorrect (because there is a leading forward-slash that is url-encoded):

```
http://127.0.0.1:9001/urlinfo/1/nestedsite.com%3A443/%2Fone%2Ftwo%2Fthree%2Findex.html
```

Requests to any other url, including to `urlinfo` without path and query sting information will return a 404: Not Found error.

### Response format

The response format for all valid requests is json. 

Whether or not the url is considered allowed to visit will be indicted by the `status` field:

- ALLOWED: URL has an entry in the database and is considered safe to visit.
- DISALLOWED: URL has an entry in the database and is considered **not** safe to visit.
- NO INFO: There is no entry for the URL in the database. The calling service should decide whether or not to let the request complete.

As an additional confirmation, the URL checked is indicated via the `url_checked` field, where it is split into `host_and_port` and `path_and_qs`. Values in these fields are **not** urlencoded.

All calls to `/urlinfo/1/` should return **HTTP 200: OK** regardless of the status of the destination URL. Other response codes indicate errors in the service (or other conditions as indicated by the HTTP code).

## Testing and type checking

urllookup includes unit tests using Python's [unittest](https://docs.python.org/3/library/unittest.html) as well as static type checking with [mypy](https://mypy.readthedocs.io/en/latest/).

### Running unit tests

To run all of urllookup's unit tests:

```
$ python -m unittest
```
**Note**: If you run the entire test suite but there is not a redis cluster available, the end-to-end tests for the redis-based lookup will be skipped.

Currently, the end-to-end tests for redis-based lookup expect to find a redis instance at `127.0.0.1:6379` and this cannot be configured by the user without changing code.

You can also run specific unit tests. For example, to run only the End2EndLocalTestCase:

```
python -m unittest tests.test_end_to_end.End2EndLocalTestCase
```

### Static type checking

To do basic type checking with mypy use:

```
$ mypy run.py
```

You can also check all of urllookup's code with:

```
$ mypy -m urllookup
```

### Load testing

In the root of the project directory you'll find `urls-to-test.txt`, which includes a list of urls you can use for load or smoke testing.

I've been using Siege for very basic load testing:

```
$ siege -c100 -r40 -f ./urls-to-test.txt
```
