class PurchasedBooksQueries:
    INSERT_PURCHASE = """
        INSERT INTO purchased_books (
            purchase_id,
            user_id,
            book_id,
            purchase_status,
            reserved_at,
            reservation_expires_at,
            total_buy_cost,
            all_fees_captured,
            meetup_time_window,
            meetup_location,
            meetup_date
        )
        VALUES (
            gen_random_uuid(),
            %s,  -- user_id
            %s,  -- book_id
            'pending',  -- purchase_status
            %s,  -- reserved_at
            %s,  -- reservation_expires_at
            %s,  -- total_buy_cost
            false,  -- all_fees_captured
            %s,  -- meetup_time_window
            %s,  -- meetup_location
            %s   -- meetup_date
        )
        RETURNING purchase_id;
    """

    CHECK_PENDING_PURCHASE = """
        SELECT 1 FROM purchased_books
        WHERE user_id = %s AND book_id = %s AND purchase_status = 'pending'
        LIMIT 1;
    """
