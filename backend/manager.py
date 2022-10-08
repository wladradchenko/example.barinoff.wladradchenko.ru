#!/usr/bin/env python
"""Aiohttp's command-line utility for administrative tasks."""
from aiohttp import web  # https://github.com/born-kh/aiohttp about db
import aiohttp_jinja2  # https://github.com/aio-libs/aiohttp-jinja2
import jinja2
from settings.urls import routes
from settings.settings import config
from clickhouse.accessor import ClickhouseAccessor
# from aiohttp_socks import SocksConnector  # onion


async def create_app(config: dict = None):
    application = web.Application()
    application["config"] = config
    aiohttp_jinja2.setup(application, loader=jinja2.PackageLoader("backend", "templates"))
    application.add_routes(routes)

    application["clickhouse"] = ClickhouseAccessor()
    application["clickhouse"].setup(application=application)

    return application


if __name__ == "__main__":
    web.run_app(create_app(config=config), port=config["port"])
    # Подключить БД - нужно отдельные либы ставить - потом
    # Можно по приколу на Clickhouse организовать
    # https://github.com/omnilib/aiosqlite
    # https://github.com/long2ice/asynch
    # https://github.com/maximdanilchenko/aiochclient
    # Научиться делать post