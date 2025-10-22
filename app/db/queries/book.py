class BookQueries:
    GET_MANY_BOOKS = (
        "SELECT * FROM books "
        "WHERE {search_by} ILIKE %s "
        "AND genre ILIKE %s "
        "AND availability::text ILIKE %s "
        "ORDER BY {sort_field} {sort_order} "
        "LIMIT %s OFFSET %s"
    )
