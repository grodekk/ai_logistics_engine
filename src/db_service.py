import os
import json
import logging
import psycopg2
from psycopg2 import sql

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
            raise


    def disconnect(self):
        if self.conn:
            self.conn.close()
            logger.info("Disconnected from the database")


    def execute(self, query, params=None):
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)

            self.conn.commit()

        except psycopg2.Error as e:
            self.conn.rollback()
            logger.error(f"Query execution error: {e}")
            raise


    def fetch_all(self, query, params=None):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


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

        except psycopg2.Error as e:
            self.conn.rollback()
            logger.error(f"Error inserting into {table}: {e}")
            raise


    def load_json(self, filepath, table, columns):
        try:
            full_path = self.build_fullpath(filepath)
            data = self.read_json(full_path)
            values = self.prepare_values(data, columns)

            self.bulk_insert(table, columns, values)

        except Exception as e:
            logger.error(f"Failed to load data from {filepath}: {e}")
            raise


    @staticmethod
    def build_fullpath(filepath):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_dir, filepath)
        return full_path


    @staticmethod
    def read_json(full_path):
        with open(full_path, encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError(f"{full_path} must be a list of objects")

        if not data:
            raise ValueError("File is empty")

        return data


    @staticmethod
    def prepare_values(data, columns):
        return [tuple(row.get(col, 0) for col in columns) for row in data]