class BookQueries:
    GET_MANY_BOOKS = (
        "SELECT b.*, u.username AS owner_username "
        "FROM books AS b "
        "JOIN users AS u ON b.owner_id = u.user_id "
        "LEFT JOIN book_genre_links AS bgl ON b.book_id = bgl.book_id "
        "LEFT JOIN book_genres AS bg ON bgl.book_genre_id = bg.book_genre_id "
        "LEFT JOIN purchased_books AS pb ON b.book_id = pb.book_id "
        "LEFT JOIN rented_books AS rb ON b.book_id = rb.book_id "
        "WHERE b.{search_by} ILIKE %s "
        "AND bg.book_genre_name ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id != %s "
        "AND (pb.purchase_status = 'pending' OR pb.purchase_status IS NULL) "
        "AND (rb.rent_status = 'pending' OR rb.rent_status IS NULL) "
        "ORDER BY {sort_field} {sort_order} "
        "LIMIT %s OFFSET %s"
    )

    GET_BOOKS_COUNT = (
        "SELECT COUNT(b.*) "
        "FROM books AS b "
        "JOIN users AS u ON b.owner_id = u.user_id "
        "LEFT JOIN book_genre_links AS bgl ON b.book_id = bgl.book_id "
        "LEFT JOIN book_genres AS bg ON bgl.book_genre_id = bg.book_genre_id "
        "LEFT JOIN purchased_books AS pb ON b.book_id = pb.book_id "
        "LEFT JOIN rented_books AS rb ON b.book_id = rb.book_id "
        "WHERE b.{search_by} ILIKE %s "
        "AND bg.book_genre_name ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id != %s "
        "AND (pb.purchase_status = 'pending' OR pb.purchase_status IS NULL) "
        "AND (rb.rent_status = 'pending' OR rb.rent_status IS NULL) "
    )
