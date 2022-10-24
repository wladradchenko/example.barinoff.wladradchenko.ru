"""Views of main pages."""
from aiohttp import web
import aiohttp_jinja2
from sqlalchemy.future import select
import postgresql.model as model


"""
Step now. Create frontend for main page. Add data to tables. Construct main page
"""
class Handler(web.View):
    """
    Main page of Web-site. (can be personal)
    """
    __slots__ = ("name", "types")

    def __init__(self, request: web.Request = None):
        super().__init__(request)

    @staticmethod
    async def get(request: web.Request):
        name = request.match_info.get('name', "Anonymous")  # filter by author name

        """Get data from PostgreSQL tables by ORM"""
        async with request.app["postgresql"].client() as session:
            products = await session.execute(select(model.Product).order_by(model.Product.id))
            await session.commit()
        """Get data from PostgreSQL tables by ORM"""

        """Get data from Clickhouse tables by SQL"""
        msg = [row for row in await request.app["clickhouse"].client.fetch("SELECT * FROM auction")]
        """Get data from Clickhouse tables by SQL"""

        context = {'name': name, 'surname': 'Svetlov', 'products': [product for product in products], 'msg': msg}
        response = aiohttp_jinja2.render_template('/main/html/main.html', request, context)
        response.headers['Content-Language'] = 'ru'

        return response

    @staticmethod
    async def post(request: web.Request):
        message = await request.post()
        """How add data in PostgreSQL by ORM"""
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
        """How add data in PostgreSQL by ORM"""

        """How add data in Clickhouse by SQL"""
        # await request.app["clickhouse"].client.execute("INSERT INTO auction VALUES", (datetime.now(), message.get("message")), )
        print("clickhouse", message.get("message"))
        """How add data in Clickhouse by SQL"""

        if request.match_info.get("name"):
            return web.HTTPFound(f'/{request.match_info.get("name")}')
        return web.HTTPFound('/')


class Product(web.View):
    """
    Product page of Web-site.
    """
    __slots__ = ("name", "types")

    def __init__(self, request: web.Request = None):
        super().__init__(request)

    @staticmethod
    async def get(request: web.Request):
        name = request.match_info.get('name', "Anonymous")    # filter by author name and product id
        product_id = request.match_info.get('product_id', "Zero")
        msg = [row for row in await request.app["clickhouse"].client.fetch("SELECT * FROM auction")]
        context = {'name': name, 'surname': product_id, 'msg': msg}
        response = aiohttp_jinja2.render_template('/main/html/product.html', request, context)
        response.headers['Content-Language'] = 'ru'

        return response

    @staticmethod
    async def post(request: web.Request):
        message = await request.post()
        # await request.app["clickhouse"].client.execute("INSERT INTO auction VALUES", (datetime.now(), message.get("message")), )
        print("clickhouse", message.get("message"))
        return web.HTTPFound(f'/{request.match_info.get("name")}/{request.match_info.get("product_id")}')