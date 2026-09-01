from src.core.config import Config
from src.core.logger_config import configure_logging
from src.db.db_service import DatabaseService


def main():
    configure_logging()
    db_service = DatabaseService(Config())

    try:
        db_service.connect()
        db_service.create_tables()
        db_service.create_views()
        print("Database initialized successfully!")

    finally:
        db_service.disconnect()


if __name__ == "__main__":
    main()
