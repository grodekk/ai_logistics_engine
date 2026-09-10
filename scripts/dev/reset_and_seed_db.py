import asyncio
import selectors

from src.core.config import Config
from src.core.logger_config import configure_logging
from src.core.paths import data_path
from src.db.db_service import DatabaseService
from src.etl.extract.json_extractor import JSONExtractor
from src.etl.extract.json_loader import JsonLoader
from src.etl.load.db_loader import DBLoader


async def main():
    configure_logging()
    confirm = input("This will DROP and recreate database tables. Type RESET to continue: ")

    if confirm != "RESET":
        print("Aborted.")
        return

    config = Config()
    db_service = DatabaseService(config)
    db_loader = DBLoader(db_service)
    json_loader = JsonLoader()
    extractor = JSONExtractor(json_loader)

    try:
        await db_service.connect()
        await db_service.execute("DROP TABLE IF EXISTS routes_costs, monthly_costs, clients, clients_routes CASCADE")
        await db_service.create_tables()
        await db_service.create_views()

        json_files = [
            (
                "monthly_costs.json",
                "monthly_costs",
                ["cost_name", "amount"],
            ),
            (
                "routes_costs.json",
                "routes_costs",
                ["route_name", "fuel", "tolls", "ferry", "hotel"],
            ),
            (
                "clients.json",
                "clients",
                [
                    "client_name",
                    "client_class",
                    "avg_payment_delay_days",
                    "late_payment_count",
                ],
            ),
            (
                "clients_routes.json",
                "clients_routes",
                ["client_name", "route_name", "shipments"],
            ),
        ]

        for filepath, table, columns in json_files:
            full_path = data_path(filepath)
            df = extractor.load_json_to_df(full_path)

            if table == "routes_costs":
                df = df.reindex(columns=columns, fill_value=0)
                df.fillna(0, inplace=True)

            await db_loader.insert_dataframe(table, df, columns)

        print("Database reset and seeded successfully!")

    finally:
        await db_service.disconnect()


def create_event_loop():
    return asyncio.SelectorEventLoop(selectors.SelectSelector())


if __name__ == "__main__":
    asyncio.run(main(), loop_factory=create_event_loop)
