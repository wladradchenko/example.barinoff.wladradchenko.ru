import asyncio
from aiohttp import web
from gino import Gino

app = web.Application()
db = Gino()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fullname = db.Column(db.String)

async def main():
    async with db.with_bind('postgres://postgres:postgres@localhost/barinoff') as engine:
        await db.gino.create_all()
        # await User.create(name='jack', fullname='Jack Jones')
        # print(await User.query.gino.all())

asyncio.get_event_loop().run_until_complete(main())

if __name__ == '__main__':
    web.run_app(app)