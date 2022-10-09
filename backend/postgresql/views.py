"""Views of main pages."""
from aiohttp import web
import aiohttp_jinja2
from sqlalchemy.future import select
import postgresql.model as model


class Handler(web.View):
    __slots__ = ("name", "types")

    def __init__(self, request: web.Request = None):
        super().__init__(request)

    @staticmethod
    async def get(request: web.Request):
        name = request.match_info.get('name', "Anonymous")
        async with request.app["postgresql"].client() as session:
            products = await session.execute(select(model.Product).order_by(model.Product.product_id))
            music_list = await session.execute(select(model.MusicList).order_by(model.MusicList.id))
            await session.commit()

        context = {'name': name, 'surname': 'Svetlov', 'products': products.scalars(), 'music': music_list.scalars()}
        response = aiohttp_jinja2.render_template('/main/html/main.html', request, context)
        response.headers['Content-Language'] = 'ru'

        return response

    @staticmethod
    async def post(request: web.Request):
        message = await request.post()
        # async with request.app["postgresql"].client() as session:
        #     async with session.begin():
        #         session.add_all(
        #             [
        #                 model.Message(msg=message.get("message")),
        #                 model.Message(msg="Test!!!"),
        #             ]
        #         )
        #     await session.commit()
        print("postgre", message.get("message"))
        return web.HTTPFound('/')
