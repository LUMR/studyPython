import asyncio

from aiohttp import web
import logging

from aiohttp.web_runner import AppRunner

from lumr_web.web import add_routes
from lumr_web.middleware import logger_factory, response_factory

if __name__ == '__main__':
    def init(loop):
        app = web.Application(loop=loop, middlewares=[logger_factory, response_factory])
        add_routes(app, 'handlers')

        srv = yield from loop.create_server(AppRunner(app)._make_server(), 'localhost', 8000)
        logging.info('server started at http://127.0.0.1:8000...')
        return srv
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
