"""Urls of all pages."""
from aiohttp import web
from postgresql.views import Handler


routes = [
    web.get('/', Handler().get),  # web.post()
    web.get('/{name}', Handler().get),
    web.post('/', Handler().post),
    web.static('/static', 'static', name='static')
]