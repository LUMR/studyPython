import asyncio
import logging

from aiohttp import web


@asyncio.coroutine
def logger_factory(app,handler):
    @asyncio.coroutine
    def logger(request):
        logging.info('Request :%s %s'%(request.method,request.path))
        return (yield from handler(request))
    return logger


@asyncio.coroutine
def response_factory(app,handler):
    @asyncio.coroutine
    def response(request):
        r = yield from handler(request)
        if isinstance(r,web.StreamResponse):
            return r
        if isinstance(r,bytes):
            resp = web.Response(body=r)
            resp.content_type='application/octet-stream'
            return resp
        if isinstance(r,str):
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp