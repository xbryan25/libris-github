class BookQueries:
    GET_BOOKS_FOR_BOOK_LIST = (
        "SELECT DISTINCT ON (b.book_id) "
        "b.*, u.username AS owner_username, bi.image_url AS first_image_url "
        "FROM books AS b "
        "JOIN users AS u ON b.owner_id = u.user_id "
        "LEFT JOIN user_address AS ua ON u.user_id = ua.user_id "
        "LEFT JOIN book_genre_links AS bgl ON b.book_id = bgl.book_id "
        "LEFT JOIN book_genres AS bg ON bgl.book_genre_id = bg.book_genre_id "
        "LEFT JOIN book_images AS bi ON b.book_id = bi.book_id AND bi.order_num = 1 "
        "WHERE b.{search_by} ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id != %s "
        "AND b.is_soft_deleted != TRUE "
        "AND NOT EXISTS ("
        "    SELECT 1 FROM rented_books rb2 "
        "    WHERE rb2.book_id = b.book_id "
        "    AND rb2.rent_status IN ('approved', 'awaiting_pickup_confirmation', 'ongoing')"
        ") "
        "AND NOT EXISTS ("
        "    SELECT 1 FROM purchased_books pb2 "
        "    WHERE pb2.book_id = b.book_id "
        "    AND pb2.original_owner_id = b.owner_id "
        "    AND pb2.purchase_status IN ('approved', 'awaiting_pickup_confirmation', 'completed')"
        "    AND pb2.ownership_transferred = FALSE"
        ") "
        "AND ("
        "    %s = '%%' "
        "    OR EXISTS ("
        "        SELECT 1 FROM book_genre_links bgl2 "
        "        JOIN book_genres bg2 ON bgl2.book_genre_id = bg2.book_genre_id "
        "        WHERE bgl2.book_id = b.book_id "
        "        AND bg2.book_genre_name ILIKE %s"
        "    )"
        ") "
        "{price_filter} "
        "{distance_filter} "
        "ORDER BY b.book_id, {sort_field} {sort_order} "
        "LIMIT %s OFFSET %s"
    )

    GET_BOOKS_FOR_BOOK_LIST_FROM_A_SPECIFIC_USER = (
        "SELECT DISTINCT ON (b.book_id) "
        "b.*, u.username AS owner_username, bi.image_url AS first_image_url "
        "FROM books AS b "
        "JOIN users AS u ON b.owner_id = u.user_id "
        "LEFT JOIN user_address AS ua ON u.user_id = ua.user_id "
        "LEFT JOIN book_genre_links AS bgl ON b.book_id = bgl.book_id "
        "LEFT JOIN book_genres AS bg ON bgl.book_genre_id = bg.book_genre_id "
        "LEFT JOIN book_images AS bi ON b.book_id = bi.book_id AND bi.order_num = 1 "
        "WHERE b.{search_by} ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id = %s "
        "AND b.is_soft_deleted != TRUE "
        "AND NOT EXISTS ("
        "    SELECT 1 FROM rented_books rb2 "
        "    WHERE rb2.book_id = b.book_id "
        "    AND rb2.rent_status IN ('approved', 'awaiting_pickup_confirmation', 'ongoing')"
        ") "
        "AND NOT EXISTS ("
        "    SELECT 1 FROM purchased_books pb2 "
        "    WHERE pb2.book_id = b.book_id "
        "    AND pb2.original_owner_id = b.owner_id "
        "    AND pb2.purchase_status IN ('approved', 'awaiting_pickup_confirmation', 'completed')"
        "    AND pb2.ownership_transferred = FALSE"
        ") "
        "AND ("
        "    %s = '%%' "
        "    OR EXISTS ("
        "        SELECT 1 FROM book_genre_links bgl2 "
        "        JOIN book_genres bg2 ON bgl2.book_genre_id = bg2.book_genre_id "
        "        WHERE bgl2.book_id = b.book_id "
        "        AND bg2.book_genre_name ILIKE %s"
        "    )"
        ") "
        "{price_filter} "
        "{distance_filter} "
        "ORDER BY b.book_id, {sort_field} {sort_order} "
        "LIMIT %s OFFSET %s"
    )

    GET_BOOK_COUNT_FOR_BOOK_LIST_FROM_A_SPECIFIC_USER = (
        "SELECT COUNT(DISTINCT b.book_id) "
        "FROM books AS b "
        "JOIN users AS u ON b.owner_id = u.user_id "
        "LEFT JOIN user_address AS ua ON u.user_id = ua.user_id "
        "LEFT JOIN book_genre_links AS bgl ON b.book_id = bgl.book_id "
        "LEFT JOIN book_genres AS bg ON bgl.book_genre_id = bg.book_genre_id "
        "WHERE b.{search_by} ILIKE %s "
        "AND bg.book_genre_name ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id = %s "
        "AND b.is_soft_deleted != TRUE "
        "AND NOT EXISTS ("
        "    SELECT 1 FROM rented_books rb2 "
        "    WHERE rb2.book_id = b.book_id "
        "    AND rb2.rent_status IN ('approved', 'awaiting_pickup_confirmation', 'ongoing')"
        ") "
        "AND NOT EXISTS ("
        "    SELECT 1 FROM purchased_books pb2 "
        "    WHERE pb2.book_id = b.book_id "
        "    AND pb2.original_owner_id = b.owner_id "
        "    AND pb2.purchase_status IN ('approved', 'awaiting_pickup_confirmation', 'completed')"
        "    AND pb2.ownership_transferred = FALSE"
        ") "
        "{price_filter} "
        "{distance_filter} "
    )

    GET_BOOK_COUNT_FOR_BOOK_LIST = (
        "SELECT COUNT(DISTINCT b.book_id) "
        "FROM books AS b "
        "JOIN users AS u ON b.owner_id = u.user_id "
        "LEFT JOIN user_address AS ua ON u.user_id = ua.user_id "
        "LEFT JOIN book_genre_links AS bgl ON b.book_id = bgl.book_id "
        "LEFT JOIN book_genres AS bg ON bgl.book_genre_id = bg.book_genre_id "
        "WHERE b.{search_by} ILIKE %s "
        "AND bg.book_genre_name ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id != %s "
        "AND b.is_soft_deleted != TRUE "
        "AND NOT EXISTS ("
        "    SELECT 1 FROM rented_books rb2 "
        "    WHERE rb2.book_id = b.book_id "
        "    AND rb2.rent_status IN ('approved', 'awaiting_pickup_confirmation', 'ongoing')"
        ") "
        "AND NOT EXISTS ("
        "    SELECT 1 FROM purchased_books pb2 "
        "    WHERE pb2.book_id = b.book_id "
        "    AND pb2.original_owner_id = b.owner_id "
        "    AND pb2.purchase_status IN ('approved', 'awaiting_pickup_confirmation', 'completed')"
        "    AND pb2.ownership_transferred = FALSE"
        ") "
        "{price_filter} "
        "{distance_filter} "
    )

    GET_MY_LIBRARY_BOOKS = (
        "SELECT DISTINCT ON (b.book_id) "
        "b.*, rb.rent_status AS rent_status, rb.user_id AS renter_id, "
        "   ru.username AS renter_username, ru.profile_image_url AS renter_profile_image_url, "
        "   bi.image_url AS first_image_url "
        "FROM books AS b "
        "LEFT JOIN book_genre_links AS bgl ON b.book_id = bgl.book_id "
        "LEFT JOIN book_genres AS bg ON bgl.book_genre_id = bg.book_genre_id "
        "LEFT JOIN purchased_books AS pb ON b.book_id = pb.book_id "
        "LEFT JOIN rented_books AS rb ON b.book_id = rb.book_id "
        "LEFT JOIN users AS ru ON rb.user_id = ru.user_id "
        "LEFT JOIN book_images AS bi ON b.book_id = bi.book_id AND bi.order_num = 1 "
        "WHERE b.{search_by} ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id = %s "
        "AND b.is_soft_deleted != TRUE "
        "AND NOT EXISTS ("
        "    SELECT 1 FROM purchased_books pb2 "
        "    WHERE pb2.book_id = b.book_id "
        "    AND pb2.original_owner_id = b.owner_id "
        "    AND pb2.purchase_status IN ('approved', 'awaiting_pickup_confirmation', 'completed')"
        "    AND pb2.ownership_transferred = true"
        "    AND pb2.user_id != b.owner_id "  # Key fix: only check sales to OTHER users
        "    AND NOT EXISTS ("
        "        SELECT 1 FROM purchased_books pb3 "
        "        WHERE pb3.book_id = pb2.book_id "
        "        AND pb3.user_id = b.owner_id "  # Changed from pb2.original_owner_id
        "        AND pb3.purchase_status IN ('approved', 'awaiting_pickup_confirmation', 'completed')"
        "        AND pb3.ownership_transferred = true"
        "        AND pb3.reserved_at > pb2.reserved_at"
        "    )"
        ") "
        "AND ("
        "    %s = '%%' "
        "    OR EXISTS ("
        "        SELECT 1 FROM book_genre_links bgl2 "
        "        JOIN book_genres bg2 ON bgl2.book_genre_id = bg2.book_genre_id "
        "        WHERE bgl2.book_id = b.book_id "
        "        AND bg2.book_genre_name ILIKE %s"
        "    )"
        ") "
        "{price_filter} "
        "ORDER BY b.book_id, {sort_field} {sort_order} "
        "LIMIT %s OFFSET %s"
    )

    GET_MY_LIBRARY_BOOK_COUNT = (
        "SELECT COUNT(DISTINCT b.book_id) "
        "FROM books AS b "
        "LEFT JOIN book_genre_links AS bgl ON b.book_id = bgl.book_id "
        "LEFT JOIN book_genres AS bg ON bgl.book_genre_id = bg.book_genre_id "
        "WHERE b.{search_by} ILIKE %s "
        "AND b.availability::text ILIKE %s "
        "AND b.owner_id = %s "
        "AND b.is_soft_deleted != TRUE "
        "AND NOT EXISTS ("
        "    SELECT 1 FROM purchased_books pb2 "
        "    WHERE pb2.book_id = b.book_id "
        "    AND pb2.original_owner_id = b.owner_id "
        "    AND pb2.purchase_status IN ('approved', 'awaiting_pickup_confirmation', 'completed')"
        ") "
        "AND ("
        "    %s = '%%' "
        "    OR EXISTS ("
        "        SELECT 1 FROM book_genre_links bgl2 "
        "        JOIN book_genres bg2 ON bgl2.book_genre_id = bg2.book_genre_id "
        "        WHERE bgl2.book_id = b.book_id "
        "        AND bg2.book_genre_name ILIKE %s"
        "    )"
        ") "
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
                ARRAY_AGG(DISTINCT bg.book_genre_name)
                FILTER (WHERE bg.book_genre_name IS NOT NULL),
                ARRAY['General']::text[]
            ) AS genres,
            COUNT(DISTINCT CASE
                WHEN rb.rent_status = 'completed'
                THEN rb.rental_id
            END) AS times_rented,
            -- Check if book is currently rented (ongoing status)
            EXISTS(
                SELECT 1 FROM rented_books rb2
                WHERE rb2.book_id = b.book_id
                AND rb2.rent_status = 'ongoing'
            ) AS is_rented,
            -- Check if book has an ACTIVE purchase from the CURRENT owner
            -- Exclude completed purchases where ownership was transferred (new owner scenario)
            EXISTS(
                SELECT 1 FROM purchased_books pb
                WHERE pb.book_id = b.book_id
                AND pb.original_owner_id = b.owner_id
                AND (
                    -- Active purchase statuses
                    pb.purchase_status IN ('pending', 'approved', 'awaiting_pickup_confirmation')
                    -- OR completed but decision still pending
                    OR (pb.purchase_status = 'completed' AND pb.transfer_decision_pending = TRUE)
                )
            ) AS is_purchased
        FROM books b
        JOIN users u ON b.owner_id = u.user_id
        LEFT JOIN book_genre_links bgl ON b.book_id = bgl.book_id
        LEFT JOIN book_genres bg ON bgl.book_genre_id = bg.book_genre_id
        LEFT JOIN rented_books rb ON b.book_id = rb.book_id
        WHERE b.book_id = %s
        AND b.is_soft_deleted != TRUE
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
            rb.rent_end_date AS return_date,
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
        WHERE pb.user_id = %s
        AND pb.purchase_status = 'completed'
        AND pb.ownership_transferred = TRUE
    """

    GET_LENT_BOOKS = """
        SELECT
            b.book_id as id,
            b.title,
            b.author,
            bi.image_url as image,
            u.username as "by",
            rb.rent_end_date as return_date,
            rb.total_rent_cost as cost
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON rb.user_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE rb.original_owner_id = %s AND rb.rent_status IN ('ongoing')
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
        WHERE pb.original_owner_id = %s
        AND pb.purchase_status = 'completed'
        AND pb.ownership_transferred = TRUE
    """

    ADD_NEW_BOOK = """
        INSERT INTO books (
            title,
            author,
            condition,
            description,
            availability,
            daily_rent_price,
            security_deposit,
            purchase_price,
            owner_id
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        ) RETURNING book_id
    """

    EDIT_A_BOOK = """
        UPDATE books
        SET
            title = %s,
            author = %s,
            condition = %s,
            description = %s,
            availability = %s,
            daily_rent_price = %s,
            security_deposit = %s,
            purchase_price = %s
        WHERE book_id = %s;
    """

    INSERT_TO_BOOK_GENRE_LINKS = (
        "INSERT INTO book_genre_links (book_id, book_genre_id) VALUES (%s, %s)"
    )

    DELETE_FROM_BOOK_GENRE_LINKS = (
        "DELETE FROM book_genre_links WHERE book_id = %s AND book_genre_id = %s"
    )

    INSERT_TO_BOOK_IMAGES = (
        "INSERT INTO book_images (image_url, uploaded_at, order_num, book_id) "
        "VALUES (%s, %s, %s, %s)"
    )

    REMOVE_FROM_BOOK_IMAGES = (
        "DELETE FROM book_images WHERE book_id = %s AND image_url = %s"
    )

    EDIT_BOOK_ORDER_IN_BOOK_IMAGES = """
        UPDATE book_images
        SET
            order_num = %s
        WHERE book_id = %s AND image_url = %s;
    """

    CHECK_IF_BOOK_HAS_RENT_OR_PURCHASE_HISTORY = """
        SELECT 1 FROM purchased_books WHERE book_id = %s
        UNION
        SELECT 1 FROM rented_books WHERE book_id = %s;
    """

    SOFT_DELETE_A_BOOK = """
        UPDATE BOOKS
        SET
            is_soft_deleted = %s
        WHERE book_id = %s;
    """

    DELETE_A_BOOK = "DELETE FROM books WHERE book_id = %s"
