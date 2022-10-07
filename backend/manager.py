#!/usr/bin/env python
"""Aiohttp's command-line utility for administrative tasks."""
from aiohttp import web  # https://github.com/born-kh/aiohttp about db
import aiohttp_jinja2  # https://github.com/aio-libs/aiohttp-jinja2
import jinja2
from settings.urls import routes
# from aiohttp_socks import SocksConnector  # onion


async def create_app(config: dict = None):
    app = web.Application()
    app['config'] = config
    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('backend', 'templates'))
    app.add_routes(routes)

    return app


if __name__ == '__main__':
    web.run_app(create_app())
    # Подключить БД - нужно отдельные либы ставить - потом
    # Можно по приколу на Clickhouse организовать
    # https://github.com/omnilib/aiosqlite
    # https://github.com/long2ice/asynch
    # https://github.com/maximdanilchenko/aiochclient
    # Научиться делать post