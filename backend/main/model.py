"""Database."""
import aiosqlite
import asyncio
# https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart

async def create_db(path_db: str) -> None:
    async with aiosqlite.connect(path_db) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS loger ( \
                             id integer PRIMARY KEY, \
                             event STRING, \
                             start DATE,\
                             end DATE \
                          );")
        await db.commit()


async def loger_get(path_db: str):
    db = await aiosqlite.connect(path_db)
    cursor = await db.execute('SELECT * FROM loger')
    row = await cursor.fetchone()
    rows = await cursor.fetchall()
    print(rows)
    await cursor.close()
    await db.close()


if __name__ == '__main__':
    # asyncio.run(create_db("../database/db.sqlite3"))
    asyncio.run(loger_get("../database/db.sqlite3"))

