from unittest.mock import AsyncMock, MagicMock, Mock

import psycopg
import pytest

from src.core.exceptions import InfrastructureError
from src.db.db_service import DatabaseService


@pytest.fixture
def config():
    cfg = Mock()
    cfg.DB_HOST = "localhost"
    cfg.DB_PORT = 5432
    cfg.DB_NAME = "test_db"
    cfg.DB_USER = "user"
    cfg.DB_PASSWORD = "pass"
    return cfg


@pytest.fixture
def db(config):
    service = DatabaseService(config)

    pool = MagicMock()
    connection = MagicMock()
    cursor = MagicMock()

    connection_context = MagicMock()
    connection_context.__aenter__ = AsyncMock(return_value=connection)
    connection_context.__aexit__ = AsyncMock(return_value=False)
    pool.connection.return_value = connection_context

    cursor_context = MagicMock()
    cursor_context.__aenter__ = AsyncMock(return_value=cursor)
    cursor_context.__aexit__ = AsyncMock(return_value=False)
    connection.cursor.return_value = cursor_context

    pool.open = AsyncMock()
    pool.close = AsyncMock()

    cursor.execute = AsyncMock()
    cursor.fetchall = AsyncMock()
    cursor.executemany = AsyncMock()

    service.pool = pool

    return service, pool, cursor


# ---------- CONNECT ---------- #


@pytest.mark.asyncio
async def test_connect_success(db):
    service, pool, _ = db

    await service.connect()

    pool.open.assert_awaited_once_with(wait=True)


@pytest.mark.asyncio
async def test_connect_failure(db):
    service, pool, _ = db
    pool.open.side_effect = psycopg.Error("Fail")

    with pytest.raises(InfrastructureError):
        await service.connect()


# ---------- DISCONNECT ---------- #


@pytest.mark.asyncio
async def test_disconnect(db):
    service, pool, _ = db

    await service.disconnect()

    pool.close.assert_awaited_once_with()


# ---------- EXECUTE ---------- #


@pytest.mark.asyncio
async def test_execute_success_without_params(db):
    service, _, cursor = db

    await service.execute("SELECT 1")

    cursor.execute.assert_awaited_once_with("SELECT 1", None)


@pytest.mark.asyncio
async def test_execute_success_with_params(db):
    service, _, cursor = db
    query = "INSERT INTO test_table (id) VALUES (%s)"
    params = (1,)

    await service.execute(query, params)

    cursor.execute.assert_awaited_once_with(query, params)


@pytest.mark.asyncio
async def test_execute_failure(db):
    service, _, cursor = db
    cursor.execute.side_effect = psycopg.Error("SQL error")

    with pytest.raises(InfrastructureError) as error:
        await service.execute("BAD SQL")

    assert isinstance(error.value.__cause__, psycopg.Error)


# ---------- FETCH_ALL ---------- #


@pytest.mark.asyncio
async def test_fetch_all_success(db):
    service, _, cursor = db
    expected = [("row1",), ("row2",)]
    cursor.fetchall.return_value = expected

    result = await service.fetch_all("SELECT * FROM test")

    assert result == expected
    cursor.execute.assert_awaited_once_with("SELECT * FROM test", None)
    cursor.fetchall.assert_awaited_once_with()


# ---------- BULK_INSERT ---------- #


@pytest.mark.asyncio
async def test_bulk_insert_success(db):
    service, _, cursor = db
    values = [(1, 2), (3, 4)]

    await service.bulk_insert(
        "test_table",
        ["col1", "col2"],
        values,
    )

    cursor.executemany.assert_awaited_once()
    query, passed_values = cursor.executemany.await_args.args

    assert passed_values == values
    assert isinstance(query, psycopg.sql.Composed)


@pytest.mark.asyncio
async def test_bulk_insert_empty(db):
    service, pool, cursor = db

    await service.bulk_insert("test_table", ["col1"], [])

    pool.connection.assert_not_called()
    cursor.executemany.assert_not_awaited()


@pytest.mark.asyncio
async def test_bulk_insert_exception(db):
    service, _, cursor = db
    cursor.executemany.side_effect = psycopg.Error("Fail")

    with pytest.raises(InfrastructureError) as error:
        await service.bulk_insert("test_table", ["col1"], [(1,)])

    assert isinstance(error.value.__cause__, psycopg.Error)
