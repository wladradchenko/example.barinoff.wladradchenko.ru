"""Urls of all pages."""
from aiohttp import web
from postgresql.views import Handler
from clickhouse.views import Streamer


routes = [
    web.get('/', Handler().get),  # turn on postgresql menu
    web.post('/', Handler().post),
    web.get('/{name}', Streamer().get),  # clickhouse if turn on camera
    web.post('/{name}', Streamer().post),
    web.static('/static', 'static', name='static')
]