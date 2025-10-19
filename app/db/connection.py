from flask import current_app

import logging

from psycopg import OperationalError
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row, TupleRow
from psycopg.abc import Query

from typing import Any

logger = logging.getLogger(__name__)


class Database:
    """Singleton class for database connection"""

    _instance = None
    _max_retries = 2

    # type hint for mypy
    pool: ConnectionPool | None

    def __new__(cls) -> "Database":
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connect_pool()
        return cls._instance

    def _connect_pool(self) -> None:
        """Initialize a connection pool."""

        if hasattr(self, "pool") and self.pool is not None and not self.pool.closed:
            self.pool.close()

        self.pool = ConnectionPool(
            conninfo=current_app.config["DATABASE_URL"],
            max_size=5,
            kwargs={"row_factory": dict_row},
        )

    def get_conn(self) -> Any:
        """Get a pooled connection (context-managed). Reconnect if pool closed."""
        if self.pool is None or self.pool.closed:
            self._connect_pool()

        assert self.pool is not None
        return self.pool.connection()

    def execute_query(self, query: Query, params: Any = None) -> None:
        """For INSERT, UPDATE, DELETE queries."""
        for attempt in range(self._max_retries + 1):
            try:
                with self.get_conn() as conn:
                    conn.autocommit = True
                    with conn.cursor() as cur:
                        cur.execute(query, params)
                return
            except OperationalError:
                if attempt < self._max_retries:
                    logger.warning(
                        f"OperationalError on attempt {attempt+1}, reconnecting..."
                    )
                    self._connect_pool()
                else:
                    raise
            except Exception as e:
                raise e
        return None

    def fetch_all(self, query: Query, params: Any = None) -> list[TupleRow] | None:
        """For SELECT queries returning multiple rows."""
        for attempt in range(self._max_retries + 1):
            try:
                with self.get_conn() as conn:
                    conn.autocommit = True
                    with conn.cursor() as cur:
                        cur.execute(query, params)
                        return cur.fetchall()
            except OperationalError:
                if attempt < self._max_retries:
                    logger.warning(
                        f"OperationalError on attempt {attempt+1}, reconnecting..."
                    )
                    self._connect_pool()
                else:
                    raise
            except Exception as e:
                raise e
        return None

    def fetch_one(self, query: Query, params: Any = None) -> TupleRow | None:
        """For SELECT queries returning a single row."""
        for attempt in range(self._max_retries + 1):
            try:
                with self.get_conn() as conn:
                    conn.autocommit = True
                    with conn.cursor() as cur:
                        cur.execute(query, params)
                        return cur.fetchone()
            except OperationalError:
                if attempt < self._max_retries:
                    logger.warning(
                        f"OperationalError on attempt {attempt+1}, reconnecting..."
                    )
                    self._connect_pool()
                else:
                    raise
            except Exception as e:
                raise e
        return None

    def close(self) -> None:
        """Close the pool and reset the singleton."""
        if hasattr(self, "pool") and self.pool is not None and not self.pool.closed:
            self.pool.close()
        Database._instance = None
