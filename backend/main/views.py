"""Views of main pages."""
# Classes https://docs.aiohttp.org/en/stable/web_quickstart.html#class-based-views
from aiohttp import web
import aiohttp_jinja2
# https://pypi.org/project/aiohttp-csrf/ если добавлять оплату
# admin panel but without clickhouse
# https://aiohttp-admin2.readthedocs.io
# https://aiohttp-admin.readthedocs.io/en/latest/#
# maybe better idea do admin panel for self


class Handler(web.View):

    def __init__(self):
        pass

    async def get(self, request: web.Request):
        name = request.match_info.get('name', "Anonymous")
        # print(request.rel_url.query['sname'])  # get param from query
        # print(type(request.rel_url.query))
        context = {'name': name, 'surname': 'Svetlov'}
        response = aiohttp_jinja2.render_template('/main/html/hello.html', request, context)
        response.headers['Content-Language'] = 'ru'
        return response

    async def post(self, request: web.Request):
        message = await request.post()
        print(message.get("message"))
        return web.HTTPFound('/')
