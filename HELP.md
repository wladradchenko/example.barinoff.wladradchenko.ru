# Classes https://docs.aiohttp.org/en/stable/web_quickstart.html#class-based-views
# https://pypi.org/project/aiohttp-csrf/ если добавлять оплату
# admin panel but without clickhouse only postgresql (why not i have two db)
# https://aiohttp-admin2.readthedocs.io
# https://aiohttp-admin.readthedocs.io/en/latest/#
# maybe better idea do admin panel for self
# https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html - sqlaclhemy
# https://habr.com/ru/company/otus/blog/683366/?ysclid=l919otk1oz769072744 - sqlaclhemy
# use yaml
# https://github.com/born-kh/aiohttp about db
# https://github.com/aio-libs/aiohttp-jinja2
# from aiohttp_socks import SocksConnector - onion


# print(request.app["config"]) - get config data from application
# print([{f'{key}: {value}' for key, value in row.items()} for row in await request.app["clickhouse"].client.fetch("SELECT * FROM message")]) - if u want to get keys and values from qury to change them
# print(request.rel_url.query['sname']) - get param from query in url
# session.add(model.Message(msg=message.get("message"))) - add only one row

# maybe it will be one page with postgre+clickhouse

