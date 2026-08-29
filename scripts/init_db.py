from src.config import Config
from src.db.db_service import DatabaseService


def main():
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