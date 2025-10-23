class BookQueries:
    GET_MANY_BOOKS = (
        "SELECT b.*, u.username AS owner_username "
        "FROM books as b "
        "JOIN users as u ON b.owner_id = u.user_id "
        "WHERE b.{search_by} ILIKE %s "
        "AND b.genre ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id != %s "
        "ORDER BY {sort_field} {sort_order} "
        "LIMIT %s OFFSET %s"
    )
