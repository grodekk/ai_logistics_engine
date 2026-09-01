import logging

import psycopg2
from psycopg2 import sql

from src.core.exceptions import InfrastructureError
from src.core.paths import SQL_DIR
from src.db.sql_loader import SQLLoader

logger = logging.getLogger(__name__)


class DatabaseService:
    def __init__(self, config):
        self.config = config
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                dbname=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
            )
            logger.info("Connected to the database")

        except psycopg2.Error as e:
            self._handle_db_error(e, context="connect")

    def _ensure_connection(self):
        if self.conn is None or self.conn.closed:
            self.connect()

    def disconnect(self):
        if self.conn:
            self.conn.close()
            logger.info("Disconnected from the database")

    def execute(self, query, params=None):
        self._run_query(query, params)

    def fetch_all(self, query, params=None):
        return self._run_query(query, params, fetch_all=True)

    def _run_query(self, query, params=None, fetch_all=False):
        self._ensure_connection()
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                if fetch_all:
                    return cur.fetchall()
                self.conn.commit()

        except psycopg2.InterfaceError as e:
            self._handle_connection_error(e)

        except psycopg2.Error as e:
            self._handle_db_error(e, query)

    def create_tables(self):
        sql_loader = SQLLoader(SQL_DIR)

        ordered_tables = [
            sql_loader.tables.routes_costs,
            sql_loader.tables.clients,
            sql_loader.tables.monthly_costs,
            sql_loader.tables.clients_routes,
        ]

        for sql_item in ordered_tables:
            try:
                self.execute(sql_item)

            except Exception as e:
                logger.error(f"[tables] SQL execution error: {e}")
                raise InfrastructureError(
                    message=f"Error executing SQL for tables: {e}",
                    user_message="Error setting up tables. Please contact support.",
                )

    def create_views(self):
        sql_loader = SQLLoader(SQL_DIR)

        for sql_item in vars(sql_loader.views).values():
            try:
                self.execute(sql_item)

            except Exception as e:
                logger.error(f"[views] SQL execution error: {e}")
                raise InfrastructureError(
                    message=f"Error executing SQL for views: {e}",
                    user_message="Error setting up views. Please contact support.",
                )

    def bulk_insert(self, table, columns, values):
        if not values:
            return

        self._ensure_connection()
        query = self._build_insert_query(table, columns)
        try:
            with self.conn.cursor() as cur:
                self._execute_bulk(cur, query, values)

            self.conn.commit()
            logger.info(f"Inserted {len(values)} rows into {table}")

        except psycopg2.Error as e:
            self._handle_db_error(e, context="connect")

    @staticmethod
    def _build_insert_query(table, columns):
        placeholders = ", ".join(["%s"] * len(columns))
        return sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table), sql.SQL(", ").join(map(sql.Identifier, columns)), sql.SQL(placeholders)
        )

    @staticmethod
    def _execute_bulk(cur, query, values):
        cur.executemany(query, values)

    def _handle_db_error(self, e, context):
        self.conn.rollback() if self.conn else None
        logger.error(f"Database error during {context}: {e}")
        raise InfrastructureError(
            message=f"Database error during {context}: {e}", user_message="Database error. Please contact support."
        )

    @staticmethod
    def _handle_connection_error(e):
        logger.error(f"Connection error: {e}")
        raise InfrastructureError(
            message=f"Connection closed: {e}", user_message="Database connection lost. Please try again."
        )
