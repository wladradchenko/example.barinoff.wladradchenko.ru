"""Accessor to PostgreSQL database."""
from aiohttp import web
import logging
from postgresql.model import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


class PostgreSQLAccessor:
    """
    PostgreSQL Accessor
    """
    def __init__(self) -> None:
        """
        Initialization
        """
        self.base = Base

        self._session = None
        self.client = None

    def setup(self, application: web.Application) -> None:
        """
        Setup startup and cleanup connection for session
        :param application: web application
        :return:
        """
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)

    async def _init_models(self):
        async with self._session.begin() as conn:
            # await conn.run_sync(self.base.metadata.drop_all)
            await conn.run_sync(self.base.metadata.create_all)

    async def _table_not_exist(self):
        pass

    async def _on_connect(self, application: web.Application):
        """
        Connection to PostgreSQL on
        :param application: web application
        :return:
        """
        self.config = application["config"]["postgres"]
        self._session = create_async_engine(self.config["database_url"], echo=True)
        await self._init_models()
        self.client = sessionmaker(self._session, class_=AsyncSession, expire_on_commit=False)

        print(f"Is PostgreSQL alive? -> {True}")
        logging.info(msg=f"List of PostgreSQL tables after start -> {[table for table in self.base.metadata.tables.keys()]}")


    async def _on_disconnect(self, _) -> None:
        """
        Connection to PostgreSQL off
        :param _: async off
        :return:
        """
        if self._session is not None:
            await self.client().close()
            await self._session.dispose()
            print("Session PostgreSQL is None")
