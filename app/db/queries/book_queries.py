class BookQueries:
    BOOK_DETAILS = """
            SELECT
                b.book_id,
                b.title,
                b.author,
                b.genre,
                b.condition,
                b.description,
                b.availability,
                b.daily_rent_price,
                b.security_deposit,
                b.purchase_price,
                u.username as owner_username,
                u.trust_score as owner_trust_score
            FROM books b
            JOIN users u ON b.owner_id = u.user_id
            WHERE b.book_id = %s
            """

    BOOK_IMAGES = """
        SELECT image_url, order_num
        FROM book_images
        WHERE book_id = %s
        ORDER BY order_num
    """

    RENTED_BOOKS = """
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

    BOUGHT_BOOKS = """
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

    LENT_BOOKS = """
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

    SOLD_BOOKS = """
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
