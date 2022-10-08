"""Accessor to Clickhouse database."""
from aiochclient import ChClient
from aiohttp import ClientSession
from aiohttp import web
import logging
from clickhouse.model import TableCreator


class ClickhouseAccessor:
    """
    Clickhouse Accessor
    """
    def __init__(self) -> None:
        """
        Initialization
        """
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

    async def _table_not_exist(self):
        """
        Method to create tables from model if ones not exist
        :return: True
        """
        logging.info(msg=f"List of tables before start -> {[row.get('name') for row in await self.client.fetch('show tables')]}")
        tables = TableCreator().sql_constructor()
        [await self.client.execute(sql) for sql in tables]
        logging.info(msg=f"List of tables after start -> {[row.get('name') for row in await self.client.fetch('show tables')]}")
        return True

    async def _on_connect(self, application: web.Application):
        """
        Connection to Clickhouse on
        :param application: web application
        :return:
        """
        self.config = application["config"]["clickhouse"]
        self._session = ClientSession(raise_for_status=True)
        self.client = ChClient(self._session, url=self.config["url"], user=self.config["user"], password=self.config["password"], database=self.config["database"], compress_response=self.config["compress_response"])
        print(f"Is ClickHouse alive? -> {await self.client.is_alive()}")
        print(f"Inspect tables -> {await self._table_not_exist()}")

    async def _on_disconnect(self, _) -> None:
        """
        Connection to Clickhouse off
        :param _: async off
        :return:
        """
        if self._session is not None:
            await self._session.close()
            print("Session is None")
