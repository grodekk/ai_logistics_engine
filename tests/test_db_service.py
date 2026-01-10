import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from src.db_service import DatabaseService
import psycopg2


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
    service.conn = MagicMock()
    return service


# ---------- CONNECT ---------- #

def test_connect_success(config):
    with patch('src.db_service.psycopg2.connect', return_value=MagicMock()) as mock_connect:
        db = DatabaseService(config)
        db.connect()
        assert db.conn is not None
        mock_connect.assert_called_once()


def test_connect_failure(config):
    with patch('src.db_service.psycopg2.connect', side_effect=psycopg2.Error("Fail")):
        db = DatabaseService(config)
        with pytest.raises(psycopg2.Error):
            db.connect()


# ---------- DISCONNECT ---------- #

def test_disconnect(db):
    db.disconnect()
    db.conn.close.assert_called_once()


# ---------- EXECUTE ---------- #

def test_execute_success_without_params(db):
    db.execute("SELECT 1")
    db.conn.cursor().__enter__().execute.assert_called_once()
    db.conn.commit.assert_called_once()


def test_execute_success_with_params(db):
    query = "INSERT INTO test_table (id) VALUES (%s)"
    params = (1,)
    db.execute(query, params)
    db.conn.cursor().__enter__().execute.assert_called_once_with(query, params)
    db.conn.commit.assert_called_once()


def test_execute_failure(db):
    db.conn.cursor().__enter__().execute.side_effect = psycopg2.Error("SQL error")
    with pytest.raises(psycopg2.Error):
        db.execute("BAD SQL")

    db.conn.rollback.assert_called_once()


# ---------- FETCH_ALL ---------- #

def test_fetch_all_success(db):
    expected = [("row1",), ("row2",)]
    db.conn.cursor().__enter__().fetchall.return_value = expected
    result = db.fetch_all("SELECT * FROM test")
    assert result == expected


# ---------- BULK_INSERT ---------- #

def test_bulk_insert_success(db):
    db.bulk_insert("test_table", ["col1", "col2"], [(1, 2), (3, 4)])
    db.conn.cursor().__enter__().executemany.assert_called_once()
    db.conn.commit.assert_called_once()


def test_bulk_insert_empty(db):
    db.bulk_insert("test_table", ["col1"], [])
    db.conn.cursor().__enter__().executemany.assert_not_called()


def test_bulk_insert_exception(db):
    db.conn.cursor().__enter__().executemany.side_effect = psycopg2.Error("Fail")
    with pytest.raises(psycopg2.Error):
        db.bulk_insert("test_table", ["col1"], [(1,)])

    db.conn.rollback.assert_called_once()


# ---------- LOAD_JSON ---------- #

def test_load_json_raises_exception(db):
    with patch.object(db, 'read_json', side_effect=ValueError("Bad file")):
        with pytest.raises(ValueError, match="Bad file"):
            db.load_json("dummy.json", "table", ["col"])


# ---------- READ_JSON ---------- #

def test_read_json_invalid_type(db):
    with patch('builtins.open', mock_open(read_data='{"not": "a list"}')):
        with pytest.raises(ValueError, match="must be a list of objects"):
            db.read_json("dummy.json")


def test_read_json_empty_file(db):
    with patch('builtins.open', mock_open(read_data='[]')):
        with pytest.raises(ValueError, match="File is empty"):
            db.read_json("dummy.json")


# ---------- PREPARE_VALUES ---------- #

def test_prepare_values():
    data = [{"a": 1, "b": 2}, {"a": 3}]
    columns = ["a", "b"]
    result = DatabaseService.prepare_values(data, columns)
    assert result == [(1, 2), (3, 0)]