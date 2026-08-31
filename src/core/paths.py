from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
SQL_DIR = BASE_DIR / "src" / "sql"


def data_path(filename: str) -> Path:
    return DATA_DIR / filename


def sql_path(filename: str) -> Path:
    return SQL_DIR / filename