import logging
import psycopg2
from psycopg2 import sql
from pathlib import Path
from src.json_loader import JsonLoader
from src.exceptions import InfrastructureError

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
        queries = [
            """
            CREATE TABLE IF NOT EXISTS monthly_costs (
                id SERIAL PRIMARY KEY,
                cost_name TEXT NOT NULL,
                amount NUMERIC(10, 2) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS routes_costs (
                id SERIAL PRIMARY KEY,
                route_name TEXT NOT NULL,
                fuel NUMERIC(10, 2) NOT NULL,
                tolls NUMERIC(10, 2) DEFAULT 0,
                ferry NUMERIC(10, 2) DEFAULT 0,
                hotel NUMERIC(10, 2) DEFAULT 0
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                client_name TEXT NOT NULL,
                client_class TEXT NOT NULL,
                avg_payment_delay_days INTEGER DEFAULT 0,
                late_payment_count INTEGER DEFAULT 0,
                total_shipments INTEGER DEFAULT 0
            );
            """
        ]
        for query in queries:
            self.execute(query)

        logger.info("Tables created successfully")


    def bulk_insert(self, table, columns, values):
        if not values:
            return

        self._ensure_connection()
        try:
            placeholders = ', '.join(['%s'] * len(columns))
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(placeholders)
            )
            with self.conn.cursor() as cur:
                cur.executemany(query, values)

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


    def insert_json_into_table(self, filepath, table, columns):
        full_path = str(self.build_fullpath(filepath))
        data = JsonLoader(full_path).load()
        values = self.prepare_values(data, columns)
        self.bulk_insert(table, columns, values)


    @staticmethod
    def build_fullpath(filepath):
        base_dir = Path(__file__).resolve().parent.parent
        data_dir = base_dir / "data"
        return data_dir / filepath


    @staticmethod
    def prepare_values(data, columns):
        return [tuple(row.get(col, 0) for col in columns) for row in data]