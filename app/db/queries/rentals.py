class RentalQueries:
    GET_USER_RENTALS_WITH_STATUS = """
        SELECT
            rb.rental_id,
            rb.rent_status,
            b.book_id,
            b.title,
            b.author,
            bi.image_url AS image,
            u.username AS "from",
            rb.all_fees_captured,
            rb.reserved_at,
            rb.reservation_expires_at,
            rb.rent_start_date,
            rb.rent_end_date,
            rb.rental_duration_days,
            rb.meetup_location,
            rb.meetup_time_window,
            rb.meetup_time,
            rb.meetup_date,
            rb.pickup_confirmation_started_at,
            rb.user_confirmed_pickup,
            rb.owner_confirmed_pickup,
            rb.return_confirmation_started_at,
            rb.user_confirmed_return,
            rb.owner_confirmed_return,
            rb.total_rent_cost AS cost
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON b.owner_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE rb.user_id = %s
        AND rb.rent_status IN ('pending', 'approved', 'awaiting_pickup_confirmation',
        'ongoing', 'awaiting_return_confirmation', 'rate_user');
    """

    GET_USER_LENDINGS_WITH_STATUS = """
         SELECT
            rb.rental_id,
            rb.rent_status,
            b.book_id,
            b.title,
            b.author,
            bi.image_url AS image,
            u.username AS "to",  -- Changed from "from" to "to" (person borrowing)
            rb.all_fees_captured,
            rb.reserved_at,
            rb.reservation_expires_at,
            rb.rent_start_date,
            rb.rent_end_date,
            rb.rental_duration_days,
            rb.meetup_date,
            rb.meetup_location,
            rb.meetup_time_window,
            rb.meetup_time,
            rb.pickup_confirmation_started_at,
            rb.user_confirmed_pickup,
            rb.owner_confirmed_pickup,
            rb.return_confirmation_started_at,
            rb.user_confirmed_return,
            rb.owner_confirmed_return,
            rb.total_rent_cost AS cost
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON rb.user_id = u.user_id  -- Changed: join to renter (user_id)
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE b.owner_id = %s
        AND rb.rent_status IN ('pending', 'approved', 'awaiting_pickup_confirmation',
        'ongoing', 'awaiting_return_confirmation', 'rate_user');
    """

    APPROVE_RENTAL = """
        UPDATE rented_books
        SET
            rent_status = 'approved',
            meetup_time = %s,
            all_fees_captured = TRUE
        WHERE rental_id = %s
        AND rent_status = 'pending'
        RETURNING rental_id, rent_status, meetup_time, all_fees_captured;
    """

    GET_RENTAL_BY_ID = """
        SELECT
            rb.rental_id,
            rb.rent_status,
            rb.user_id,
            rb.meetup_time_window,
            rb.total_rent_cost,
            b.owner_id,
            b.title
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        WHERE rb.rental_id = %s;
    """

    DELETE_RENTAL = """
    DELETE FROM rented_books
    WHERE rental_id = %s
    AND rent_status = 'pending'
    RETURNING rental_id;
"""
