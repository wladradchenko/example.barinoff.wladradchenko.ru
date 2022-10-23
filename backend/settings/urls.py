"""Urls of all pages."""
from aiohttp import web
from pages.main.views import Handler, Product  # postgresql + clickhouse
# from postgresql.views import Handler
# from clickhouse.views import Streamer


routes = [
    web.get('/', Handler().get),
    web.post('/', Handler().post),
    web.get('/{name}', Handler().get),
    web.post('/{name}', Handler().post),
    web.get('/{name}/{product_id}', Product().get),
    web.post('/{name}/{product_id}', Product().post),
    web.static('/static', 'static', name='static'),
    web.static('/media', 'media', name='media')
]