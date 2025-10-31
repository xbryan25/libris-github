class BookQueries:
    GET_BOOKS_FOR_BOOK_LIST = (
        "SELECT DISTINCT ON (b.book_id) "
        "b.*, u.username AS owner_username, bi.image_url AS first_image_url "
        "FROM books AS b "
        "JOIN users AS u ON b.owner_id = u.user_id "
        "LEFT JOIN book_genre_links AS bgl ON b.book_id = bgl.book_id "
        "LEFT JOIN book_genres AS bg ON bgl.book_genre_id = bg.book_genre_id "
        "LEFT JOIN purchased_books AS pb ON b.book_id = pb.book_id "
        "LEFT JOIN rented_books AS rb ON b.book_id = rb.book_id "
        "LEFT JOIN book_images AS bi ON b.book_id = bi.book_id AND bi.order_num = 1 "
        "WHERE b.{search_by} ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id != %s "
        "AND (pb.purchase_status = 'pending' OR pb.purchase_status IS NULL) "
        "AND (rb.rent_status = 'pending' OR rb.rent_status = 'completed' OR rb.rent_status IS NULL) "
        "AND ("
        "    %s = '%%' "
        "    OR EXISTS ("
        "        SELECT 1 FROM book_genre_links bgl2 "
        "        JOIN book_genres bg2 ON bgl2.book_genre_id = bg2.book_genre_id "
        "        WHERE bgl2.book_id = b.book_id "
        "        AND bg2.book_genre_name ILIKE %s"
        "    )"
        ") "
        "ORDER BY b.book_id, {sort_field} {sort_order} "
        "LIMIT %s OFFSET %s"
    )

    GET_BOOKS_FOR_BOOK_LIST_FROM_A_SPECIFIC_USER = (
        "SELECT DISTINCT ON (b.book_id) "
        "b.*, u.username AS owner_username, bi.image_url AS first_image_url "
        "FROM books AS b "
        "JOIN users AS u ON b.owner_id = u.user_id "
        "LEFT JOIN book_genre_links AS bgl ON b.book_id = bgl.book_id "
        "LEFT JOIN book_genres AS bg ON bgl.book_genre_id = bg.book_genre_id "
        "LEFT JOIN purchased_books AS pb ON b.book_id = pb.book_id "
        "LEFT JOIN rented_books AS rb ON b.book_id = rb.book_id "
        "LEFT JOIN book_images AS bi ON b.book_id = bi.book_id AND bi.order_num = 1 "
        "WHERE b.{search_by} ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id = %s "
        "AND (pb.purchase_status = 'pending' OR pb.purchase_status IS NULL) "
        "AND (rb.rent_status = 'pending' OR rb.rent_status = 'completed' OR rb.rent_status IS NULL) "
        "AND ("
        "    %s = '%%' "
        "    OR EXISTS ("
        "        SELECT 1 FROM book_genre_links bgl2 "
        "        JOIN book_genres bg2 ON bgl2.book_genre_id = bg2.book_genre_id "
        "        WHERE bgl2.book_id = b.book_id "
        "        AND bg2.book_genre_name ILIKE %s"
        "    )"
        ") "
        "ORDER BY b.book_id, {sort_field} {sort_order} "
        "LIMIT %s OFFSET %s"
    )

    GET_BOOK_COUNT_FOR_BOOK_LIST_FROM_A_SPECIFIC_USER = (
        "SELECT COUNT(DISTINCT b.book_id) "
        "FROM books AS b "
        "JOIN users AS u ON b.owner_id = u.user_id "
        "LEFT JOIN book_genre_links AS bgl ON b.book_id = bgl.book_id "
        "LEFT JOIN book_genres AS bg ON bgl.book_genre_id = bg.book_genre_id "
        "LEFT JOIN purchased_books AS pb ON b.book_id = pb.book_id "
        "LEFT JOIN rented_books AS rb ON b.book_id = rb.book_id "
        "WHERE b.{search_by} ILIKE %s "
        "AND bg.book_genre_name ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id = %s "
        "AND (pb.purchase_status = 'pending' OR pb.purchase_status IS NULL) "
        "AND (rb.rent_status = 'pending' OR rb.rent_status = 'completed' OR rb.rent_status IS NULL) "
    )

    GET_BOOK_COUNT_FOR_BOOK_LIST = (
        "SELECT COUNT(DISTINCT b.book_id) "
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
        "AND (rb.rent_status = 'pending' OR rb.rent_status = 'completed' OR rb.rent_status IS NULL) "
    )

    GET_BOOK_DETAILS = """
            SELECT
            b.book_id,
            b.title,
            b.author,
            b.condition,
            b.description,
            b.availability,
            b.daily_rent_price,
            b.security_deposit,
            b.purchase_price,
            u.user_id as owner_user_id,
            u.username AS owner_username,
            u.profile_image_url AS owner_profile_picture,
            u.trust_score AS owner_trust_score,
            COALESCE(
                ARRAY_AGG(DISTINCT bg.book_genre_name) FILTER (WHERE bg.book_genre_name IS NOT NULL),
                ARRAY['General']::text[]
            ) AS genres,
            COUNT(DISTINCT CASE WHEN rb.rent_status = 'completed' THEN rb.rental_id END) AS times_rented,
            -- Check if book is currently rented (ongoing status)
            EXISTS(
                SELECT 1 FROM rented_books rb2
                WHERE rb2.book_id = b.book_id
                AND rb2.rent_status = 'ongoing'
            ) AS is_rented,
            -- Check if book has been purchased (completed status)
            EXISTS(
                SELECT 1 FROM purchased_books pb
                WHERE pb.book_id = b.book_id
                AND pb.purchase_status = 'completed'
            ) AS is_purchased
        FROM books b
        JOIN users u ON b.owner_id = u.user_id
        LEFT JOIN book_genre_links bgl ON b.book_id = bgl.book_id
        LEFT JOIN book_genres bg ON bgl.book_genre_id = bg.book_genre_id
        LEFT JOIN rented_books rb ON b.book_id = rb.book_id
        WHERE b.book_id = %s
        GROUP BY
            b.book_id,
            b.title,
            b.author,
            b.condition,
            b.description,
            b.availability,
            b.daily_rent_price,
            b.security_deposit,
            b.purchase_price,
            u.user_id,
            u.username,
            u.profile_image_url,
            u.trust_score;
        """

    GET_BOOK_IMAGES = """
        SELECT image_url, order_num
        FROM book_images
        WHERE book_id = %s
        ORDER BY order_num
    """

    GET_RENTED_BOOKS = """
            SELECT
                b.book_id AS id,
                b.title,
                b.author,
                bi.image_url AS image,
                u.username AS "from",
                rb.return_due_date AS return_date,
                rb.total_rent_cost AS cost
            FROM rented_books rb
            JOIN books b ON rb.book_id = b.book_id
            JOIN users u ON b.owner_id = u.user_id
            LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
            WHERE rb.user_id = %s
            AND rb.rent_status IN ('ongoing');
            """

    GET_BOUGHT_BOOKS = """
            SELECT
                b.book_id as id,
                b.title,
                b.author,
                bi.image_url as image,
                u.username as "from",
                pb.total_buy_cost as cost
            FROM purchased_books pb
            JOIN books b ON pb.book_id = b.book_id
            JOIN users u ON b.owner_id = u.user_id
            LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
            WHERE pb.user_id = %s AND pb.purchase_status = 'completed'
            """

    GET_LENT_BOOKS = """
            SELECT
                b.book_id as id,
                b.title,
                b.author,
                bi.image_url as image,
                u.username as "by",
                rb.return_due_date as return_date,
                rb.total_rent_cost as cost
            FROM rented_books rb
            JOIN books b ON rb.book_id = b.book_id
            JOIN users u ON rb.user_id = u.user_id
            LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
            WHERE b.owner_id = %s AND rb.rent_status IN ('ongoing')
        """

    GET_SOLD_BOOKS = """
            SELECT
                b.book_id as id,
                b.title,
                b.author,
                bi.image_url as image,
                u.username as "by",
                pb.total_buy_cost as cost
            FROM purchased_books pb
            JOIN books b ON pb.book_id = b.book_id
            JOIN users u ON pb.user_id = u.user_id
            LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
            WHERE b.owner_id = %s AND pb.purchase_status = 'completed'
        """
