import logging
import psycopg2
from psycopg2 import sql
from src.exceptions import InfrastructureError
from src.etl.load.sql_loader import SQLLoader
from src.utils import SQL_DIR


logging.basicConfig(level=logging.INFO)
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


    def create_sql(self, group):
        sql_loader = SQLLoader(SQL_DIR)

        if not hasattr(sql_loader, group):
            logger.error(f"SQL group '{group}' not found in SQLLoader")
            raise InfrastructureError(
                message=f"SQL group '{group}' not found in SQLLoader",
                user_message="Internal error. Please contact support."
            )

        for sql_content in vars(getattr(sql_loader, group)).values():
            try:
                self.execute(sql_content)
            except Exception as e:
                logger.error(f"[{group}] SQL execution error: {e} | SQL: {sql_content[:50]}...")

        logger.info(f"{group} created successfully")


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
        placeholders = ', '.join(['%s'] * len(columns))
        return sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(placeholders)
        )


    @staticmethod
    def _execute_bulk(cur, query, values):
        cur.executemany(query, values)


    def _handle_db_error(self, e, context):
        self.conn.rollback() if self.conn else None
        logger.error(f"Database error during {context}: {e}")
        raise InfrastructureError(
            message=f"Database error during {context}: {e}",
            user_message="Database error. Please contact support."
        )


    @staticmethod
    def _handle_connection_error(e):
        logger.error(f"Connection error: {e}")
        raise InfrastructureError(
            message=f"Connection closed: {e}",
            user_message="Database connection lost. Please try again."
        )