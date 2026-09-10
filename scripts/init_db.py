import asyncio
import selectors

from src.core.config import Config
from src.core.logger_config import configure_logging
from src.db.db_service import DatabaseService


async def main():
    configure_logging()
    db_service = DatabaseService(Config())

    try:
        await db_service.connect()
        await db_service.create_tables()
        await db_service.create_views()
        print("Database initialized successfully!")

    finally:
        await db_service.disconnect()


def create_event_loop():
    return asyncio.SelectorEventLoop(selectors.SelectSelector())


if __name__ == "__main__":
    asyncio.run(main(), loop_factory=create_event_loop)
