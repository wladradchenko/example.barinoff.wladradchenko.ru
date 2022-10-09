#!/usr/bin/env python
"""Aiohttp's command-line utility for administrative tasks."""
from aiohttp import web
import aiohttp_jinja2
import jinja2
from settings.urls import routes
from settings.settings import config
from clickhouse.accessor import ClickhouseAccessor
from postgresql.accessor import PostgreSQLAccessor


async def create_app(configure: dict = None):
    application = web.Application()
    application["config"] = configure
    aiohttp_jinja2.setup(application, loader=jinja2.PackageLoader("backend", "templates"))
    application.add_routes(routes)

    application["clickhouse"] = ClickhouseAccessor()
    application["clickhouse"].setup(application=application)

    application["postgresql"] = PostgreSQLAccessor()
    application["postgresql"].setup(application=application)

    return application


if __name__ == "__main__":
    web.run_app(create_app(configure=config), port=config["port"])
