class CommonQueries:
    """This class contains queries that can be called regardless of feature."""

    INSERT = "INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    GET_TOTAL_COUNT = "SELECT COUNT(*) FROM {table}"
    GET_TOTAL_COUNT_WITH_CONDITIONS = (
        "SELECT COUNT(*) AS count FROM {table} WHERE {conditions}"
    )
    GET_BY_ID = "SELECT * FROM {table} WHERE {pk} = %s LIMIT 1"
    GET_ALL = "SELECT * FROM {table}"
    GET_MANY = (
        "SELECT * FROM {table} "
        "WHERE {conditions} "
        "ORDER BY {sort_field} {sort_order} "
        "LIMIT %s OFFSET %s"
    )
    UPDATE_BY_ID = "UPDATE {table} SET {set_clause} WHERE {pk} = %s"
    DELETE_BY_ID = "DELETE FROM {table} WHERE {pk} = %s"
    GET_COLUMNS_FROM_TABLE = "SELECT {columns} FROM {table} ORDER BY {order_column} ASC"
    GET_BY_SPECIFIC_COLUMN = "SELECT * FROM {table} WHERE {column} = %s"
    GET_COLUMN_BY_FIELD = "SELECT {column} FROM {table} WHERE {field} = %s"
    CHECK_IF_EXISTS = "SELECT EXISTS (SELECT 1 FROM {table} WHERE {column} = %s)"
    GET_IDS_BY_VALUES = "SELECT {column} FROM {table} WHERE {field} = ANY(%s)"
