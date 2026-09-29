import logging

import psycopg
from psycopg import conninfo, sql
from psycopg_pool import AsyncConnectionPool, PoolTimeout

from src.core.exceptions import InfrastructureError
from src.core.paths import SQL_DIR
from src.db.sql_loader import SQLLoader

logger = logging.getLogger(__name__)


class DatabaseService:
    def __init__(self, config):
        connection_info = conninfo.make_conninfo(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
        )

        self.pool = AsyncConnectionPool(
            conninfo=connection_info,
            min_size=1,
            max_size=10,
            open=False,
        )

    async def connect(self):
        try:
            await self.pool.open(wait=True)
            logger.info("Connected to the database")

        except psycopg.Error as e:
            self._handle_db_error(e, context="connect")

    async def disconnect(self):
        await self.pool.close()
        logger.info("Disconnected from the database")

    async def execute(self, query, params=None):
        await self._run_query(query, params)

    async def fetch_all(self, query, params=None):
        return await self._run_query(query, params, fetch_all=True)

    async def _run_query(self, query, params=None, fetch_all=False):
        try:
            async with self.pool.connection() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(query, params)

                    if fetch_all:
                        return await cursor.fetchall()

        except PoolTimeout as e:
            self._handle_db_error(e, context="acquiring database connection")

        except psycopg.Error as e:
            self._handle_db_error(e, context=query)

    async def create_tables(self):
        sql_loader = SQLLoader(SQL_DIR)

        ordered_tables = [
            sql_loader.tables.routes_costs,
            sql_loader.tables.clients,
            sql_loader.tables.monthly_costs,
            sql_loader.tables.clients_routes,
        ]

        try:
            for sql_item in ordered_tables:
                await self.execute(sql_item)

        except InfrastructureError as e:
            raise InfrastructureError(
                message=f"Error executing SQL for tables: {e}",
                user_message="Error setting up tables. Please contact support.",
            ) from e

    async def create_views(self):
        sql_loader = SQLLoader(SQL_DIR)

        try:
            for sql_item in vars(sql_loader.views).values():
                await self.execute(sql_item)

        except InfrastructureError as e:
            raise InfrastructureError(
                message=f"Error executing SQL for views: {e}",
                user_message="Error setting up views. Please contact support.",
            ) from e

    async def bulk_insert(self, table, columns, values):
        if not values:
            return

        query = self._build_insert_query(table, columns)

        try:
            async with self.pool.connection() as connection:
                async with connection.cursor() as cursor:
                    await cursor.executemany(query, values)

            logger.info("Inserted %s rows into %s", len(values), table)

        except psycopg.Error as e:
            self._handle_db_error(e, context="bulk insert")

    @staticmethod
    def _build_insert_query(table, columns):
        columns_sql = sql.SQL(", ").join(sql.Identifier(column) for column in columns)
        placeholders_sql = sql.SQL(", ").join(sql.Placeholder() for _ in columns)

        return sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table),
            columns_sql,
            placeholders_sql,
        )

    @staticmethod
    def _handle_db_error(e, context):
        logger.error("Database error during %s: %s", context, e)

        raise InfrastructureError(
            message=f"Database error during {context}: {e}",
            user_message="Database error. Please contact support.",
        ) from e
