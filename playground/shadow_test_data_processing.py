from src.db.db_service import DatabaseService
from src.data_processing import DataProcessing
from src.config import Config

db = DatabaseService(Config())
db.connect()
dp = DataProcessing(db)

try:
    print("\nMonthly Costs")
    print(dp.get_monthly_costs())

    print("\nRoutes Costs")
    print(dp.get_routes_costs())

finally:
    db.disconnect()