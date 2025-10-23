from flask import current_app

import logging

from psycopg import OperationalError
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row, TupleRow
from psycopg.abc import Query

from typing import Any, Optional

logger = logging.getLogger(__name__)


class Database:
    """Thread-safe singleton for PostgreSQL connection pooling."""

    _instance: Optional["Database"] = None
    _max_retries = 2

    # type hint for mypy
    pool: Optional[ConnectionPool] = None

    def __new__(cls) -> "Database":
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def init_app(self, app) -> None:
        """
        Explicitly initialize the connection pool using the Flask app config.
        Should be called once from create_app().
        """
        if self.pool and not self.pool.closed:
            self.close()

        conninfo = app.config.get("DATABASE_URL")
        if not conninfo:
            raise RuntimeError("DATABASE_URL is not configured in Flask app.")

        self.pool = ConnectionPool(
            conninfo=conninfo,
            min_size=2,
            max_size=3,
            kwargs={"row_factory": dict_row},
        )

        logger.info("Database connection pool initialized")

    def get_conn(self):
        """Get a pooled connection (context-managed)."""
        if not self.pool or self.pool.closed:
            logger.warning("Connection pool was closed; reconnecting...")
            self.reconnect()
        assert self.pool is not None
        return self.pool.connection()

    def reconnect(self):
        """Reconnect using current Flask app config."""
        try:
            self.init_app(current_app)
        except RuntimeError:
            logger.error("Cannot reconnect — current_app not ready.")

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
                    self.reconnect()
                else:
                    raise

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
                    self.reconnect()
                else:
                    raise
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
                    self.reconnect()
                else:
                    raise
        return None

    def close(self):
        """Close the pool gracefully."""
        if self.pool and not self.pool.closed:
            try:
                self.pool.close()
                logger.info("Database connection pool closed cleanly")
            except Exception as e:
                logger.error(f"Error closing database pool: {e}")
            self.pool = None
            Database._instance = None
