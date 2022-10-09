"""Views of main pages."""
from aiohttp import web
import aiohttp_jinja2
# from datetime import datetime


class Streamer(web.View):
    __slots__ = ("name", "types")

    def __init__(self, request: web.Request = None):
        super().__init__(request)

    @staticmethod
    async def get(request: web.Request):
        name = request.match_info.get('name', "Anonymous")
        msg = [row for row in await request.app["clickhouse"].client.fetch("SELECT * FROM auction")]
        context = {'name': name, 'surname': 'Svetlov', 'msg': msg}
        response = aiohttp_jinja2.render_template('/main/html/product.html', request, context)
        response.headers['Content-Language'] = 'ru'

        return response

    @staticmethod
    async def post(request: web.Request):
        message = await request.post()
        # await request.app["clickhouse"].client.execute("INSERT INTO auction VALUES", (datetime.now(), message.get("message")), )
        print("clickhouse", message.get("message"))
        return web.HTTPFound(f'/{request.match_info.get("name")}')
