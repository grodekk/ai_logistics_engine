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
            logger.error(f"Connection error: {e}")
            raise InfrastructureError(
                message=f"Database connection failed: {e}",
                user_message="Database is unavailable. Please contact support."
            )


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
            logger.error(f"Connection closed: {e}")
            raise InfrastructureError(
                message=f"Connection closed: {e}",
                user_message="Database connection lost. Please try again."
            )

        except psycopg2.Error as e:
            self.conn.rollback()
            logger.error(f"Query error: {e}")
            raise InfrastructureError(
                message=f"Database query failed: {e}",
                user_message="Database error. Please contact support."
            )


    def create_tables(self):
        sql_loader = SQLLoader(SQL_DIR)

        for sql_content in vars(sql_loader.tables).values():
            self.execute(sql_content)

        logger.info("Tables created successfully")


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


        except psycopg2.InterfaceError as e:
            logger.error(f"Connection closed: {e}")
            raise InfrastructureError(
                message=f"Connection closed: {e}",
                user_message="Database connection lost. Please try again."
            )

        except psycopg2.Error as e:
            self.conn.rollback()
            logger.error(f"Error inserting into {table}: {e}")
            raise InfrastructureError(
                message=f"Bulk insert failed for {table}: {e}",
                user_message="Database error. Please contact support."
            )


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