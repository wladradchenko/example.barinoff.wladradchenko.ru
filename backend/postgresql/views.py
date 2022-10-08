"""Views of main pages."""
# Classes https://docs.aiohttp.org/en/stable/web_quickstart.html#class-based-views
from aiohttp import web
import aiohttp_jinja2
import ast
# https://pypi.org/project/aiohttp-csrf/ если добавлять оплату
# admin panel but without clickhouse
# https://aiohttp-admin2.readthedocs.io
# https://aiohttp-admin.readthedocs.io/en/latest/#
# maybe better idea do admin panel for self


class Handler(web.View):
    __slots__ = ("name", "types")

    def __init__(self, request: web.Request = None):
        super().__init__(request)

    @staticmethod
    async def get(request: web.Request):
        name = request.match_info.get('name', "Anonymous")
        # print(request.app["config"])
        msg = [row for row in await request.app["clickhouse"].client.fetch("SELECT * FROM message")]
        # print([{f'{key}: {value}' for key, value in row.items()} for row in await request.app["clickhouse"].client.fetch("SELECT * FROM message")])
        # print(request.rel_url.query['sname'])  # get param from query
        # print(type(request.rel_url.query))
        context = {'name': name, 'surname': 'Svetlov', 'msg': msg}
        response = aiohttp_jinja2.render_template('/main/html/hello.html', request, context)
        response.headers['Content-Language'] = 'ru'

        return response

    @staticmethod
    async def post(request: web.Request):
        import datetime
        message = await request.post()
        await request.app["clickhouse"].client.execute("INSERT INTO message VALUES", (datetime.datetime.now(), message.get("message")), )
        print(message.get("message"))
        return web.HTTPFound('/')
