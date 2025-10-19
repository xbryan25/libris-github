class CommonQueries:
    """This class contains queries that can be called regardless of feature."""

    INSERT = "INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    GET_TOTAL_COUNT = "SELECT COUNT(*) FROM {table}"
    GET_BY_ID = "SELECT * FROM {table} WHERE {pk} = %s LIMIT 1"
    GET_ALL = "SELECT * FROM {table}"
    GET_MANY = (
        "SELECT * FROM {table} "
        "WHERE {search_by} LIKE %s "
        "ORDER BY {sort_field} {sort_order} "
        "LIMIT %s OFFSET %s"
    )
    UPDATE_BY_ID = "UPDATE {table} SET {set_clause} WHERE {pk} = %s"
    DELETE_BY_ID = "DELETE FROM {table} WHERE {pk} = %s"
    GET_ALL_IDS = "SELECT {columns} FROM {table} ORDER BY {order_column} ASC"
    GET_BY_SPECIFIC_COLUMN = "SELECT * FROM {table} WHERE {column} = %s"
    GET_COLUMN_BY_PK = "SELECT {column} FROM {table} WHERE {pk} = %s"
    CHECK_IF_EXISTS = "SELECT EXISTS (SELECT 1 FROM {table} WHERE {column} = %s)"
    DASHBOARD_COUNTS = """
    SELECT
      (SELECT COUNT(*) FROM rented_books WHERE user_id = %s) AS books_borrowed,
      (SELECT COUNT(*) FROM rented_books WHERE user_id = %s AND rent_status = 'ongoing') AS currently_lending,
      (SELECT COUNT(*) FROM rented_books WHERE user_id = %s AND rent_status = 'pending') AS currently_renting,
      (SELECT COUNT(*) FROM purchased_books WHERE user_id = %s AND purchase_status = 'completed') AS books_sold,
      (SELECT COUNT(*) FROM purchased_books WHERE user_id = %s AND purchase_status IN ('approved', 'pending')) AS books_bought,
      (
        COALESCE((SELECT SUM(total_rent_cost) FROM rented_books WHERE user_id = %s AND rent_status = 'completed'), 0)
        + COALESCE((SELECT SUM(total_buy_cost) FROM purchased_books WHERE user_id = %s AND purchase_status = 'completed'), 0)
      ) AS total_earnings;
    """
