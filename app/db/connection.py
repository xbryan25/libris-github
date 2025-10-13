from flask import current_app

from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row, TupleRow
from psycopg.abc import Query

from typing import Any


class Database:
    """Singleton class for database connection"""

    _instance = None

    def __new__(cls) -> "Database":
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connect_pool()
        return cls._instance

    def _connect_pool(self) -> None:
        """Initialize a connection pool."""

        self.pool = ConnectionPool(
            conninfo=current_app.config["DATABASE_URL"],
            max_size=5,
            kwargs={"row_factory": dict_row},
        )

    def get_conn(self):
        """Get a pooled connection (context-managed)."""
        if self.pool.closed:
            self._connect_pool()
        return self.pool.connection()

    def execute_query(self, query: Query, params: Any = None) -> None:
        """For INSERT, UPDATE, DELETE queries."""
        try:
            with self.get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    conn.commit()
        except Exception as e:
            raise e

    def fetch_all(self, query: Query, params: Any = None) -> list[TupleRow]:
        """For SELECT queries returning multiple rows."""
        try:
            with self.get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    return cur.fetchall()
        except Exception as e:
            raise e

    def fetch_one(self, query: Query, params: Any = None) -> TupleRow | None:
        """For SELECT queries returning a single row."""
        try:
            with self.get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    return cur.fetchone()
        except Exception as e:
            raise e

    def close(self) -> None:
        """Close the pool and reset the singleton."""
        if hasattr(self, "pool") and not self.pool.closed:
            self.pool.close()
        Database._instance = None

    def test_supabase_connection(self):
        try:
            with self.get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version();")
                    row = cur.fetchone()

                    if row is not None:
                        print("✅ Connected successfully!")
                        print("PostgreSQL version:", row["version"])
                    else:
                        print("❌ Query returned no result")

        except Exception as e:
            raise e
