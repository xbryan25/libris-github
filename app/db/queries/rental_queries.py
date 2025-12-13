class RentalsQueries:
    INSERT_RENTAL = """
        INSERT INTO rented_books (
            rental_id,
            user_id,
            original_owner_id,
            book_id,
            rent_status,
            reserved_at,
            reservation_expires_at,
            total_rent_cost,
            rental_duration_days,
            all_fees_captured,
            meetup_time_window,
            meetup_location,
            latitude,
            longitude,
            meetup_date,
            actual_rate,
            actual_deposit
        )
        VALUES (
            gen_random_uuid(),
            %s,  -- user_id
            %s, -- original_owner_id
            %s,  -- book_id
            'pending',  -- rent_status
            %s,  -- reserved_at
            %s,  -- reservation_expires_at
            %s,  -- total_rent_cost
            %s,  -- rental_duration_days
            false,  -- all_fees_captured
            %s,  -- meetup_time_window
            %s,  -- meetup_location
            %s,  -- latitude
            %s,  -- longitude
            %s,  -- meetup_date
            %s,  -- actual_rate
            %s   -- actual_deposit
        )
        RETURNING rental_id;
    """

    CHECK_PENDING_RENTAL = """
    SELECT 1 FROM rented_books
    WHERE user_id = %s AND book_id = %s AND rent_status = 'pending'
    LIMIT 1;
    """

    GET_USER_RENTALS_WITH_STATUS = """
        SELECT
            rb.rental_id,
            rb.rent_status,
            rb.original_owner_id,
            rb.user_id,
            b.book_id,
            b.title,
            b.author,
            rb.actual_deposit,
            rb.actual_rate,
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
            rb.user_rated,
            rb.owner_rated,
            rb.total_rent_cost AS cost
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON rb.original_owner_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE rb.user_id = %s
        AND (
            rb.rent_status IN ('pending', 'approved', 'awaiting_pickup_confirmation',
            'ongoing', 'awaiting_return_confirmation')
            OR (rb.rent_status = 'completed' AND rb.user_rated = false)
        );
    """

    GET_COMPLETED_RENTAL = """
        SELECT
            rb.rental_id,
            rb.rent_status,
            rb.original_owner_id,
            rb.user_id,
            b.book_id,
            b.title,
            b.author,
            rb.actual_deposit,
            rb.actual_rate,
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
            rb.user_rated,
            rb.owner_rated,
            rb.total_rent_cost AS cost
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON rb.original_owner_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE rb.rental_id = %s
        AND rb.user_id = %s
        AND rb.rent_status = 'completed'
        AND rb.user_rated = true
        AND rb.owner_rated = true
    """

    GET_USER_COMPLETED_RENTALS = """
        SELECT
            rb.rental_id,
            rb.rent_status,
            rb.original_owner_id,
            rb.user_id,
            b.book_id,
            b.title,
            b.author,
            rb.actual_deposit,
            rb.actual_rate,
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
            rb.user_rated,
            rb.owner_rated,
            rb.total_rent_cost AS cost
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON rb.original_owner_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE rb.user_id = %s
        AND rb.rent_status = 'completed'
        AND rb.user_rated = true
        AND rb.owner_rated = true
        ORDER BY {sort_by} {sort_order}
        LIMIT %s OFFSET %s
    """

    GET_USER_COMPLETED_RENTALS_COUNT = """
        SELECT COUNT(*) AS count
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON rb.original_owner_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE rb.user_id = %s
        AND rb.rent_status = 'completed'
        AND rb.user_rated = true
        AND rb.owner_rated = true
    """

    GET_USER_LENDINGS_WITH_STATUS = """
        SELECT
            rb.rental_id,
            rb.rent_status,
            rb.original_owner_id,
            rb.user_id,
            b.book_id,
            b.title,
            b.author,
            rb.actual_deposit,
            rb.actual_rate,
            bi.image_url AS image,
            u.username AS "to",
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
            rb.user_rated,
            rb.owner_rated,
            rb.total_rent_cost AS cost
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON rb.user_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE rb.original_owner_id = %s
        AND (
            rb.rent_status IN ('pending', 'approved', 'awaiting_pickup_confirmation',
            'ongoing', 'awaiting_return_confirmation')
            OR (rb.rent_status = 'completed' AND rb.owner_rated = false)
        );
    """

    GET_COMPLETED_LENDING = """
        SELECT
            rb.rental_id,
            rb.rent_status,
            rb.original_owner_id,
            rb.user_id,
            b.book_id,
            b.title,
            b.author,
            rb.actual_deposit,
            rb.actual_rate,
            bi.image_url AS image,
            u.username AS "to",
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
            rb.user_rated,
            rb.owner_rated,
            rb.total_rent_cost AS cost
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON rb.user_id  = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE rb.rental_id = %s
        AND rb.original_owner_id = %s
        AND rb.rent_status = 'completed'
        AND rb.user_rated = true
        AND rb.owner_rated = true
    """

    GET_USER_COMPLETED_LENDINGS = """
        SELECT
            rb.rental_id,
            rb.rent_status,
            rb.original_owner_id,
            rb.user_id,
            b.book_id,
            b.title,
            b.author,
            rb.actual_deposit,
            rb.actual_rate,
            bi.image_url AS image,
            u.username AS "to",
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
            rb.user_rated,
            rb.owner_rated,
            rb.total_rent_cost AS cost
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON rb.user_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE rb.original_owner_id  = %s
        AND rb.rent_status = 'completed'
        AND rb.user_rated = true
        AND rb.owner_rated = true
        ORDER BY {sort_by} {sort_order}
        LIMIT %s OFFSET %s
    """

    GET_USER_COMPLETED_LENDINGS_COUNT = """
        SELECT COUNT(*) AS count
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON rb.user_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE rb.original_owner_id  = %s
        AND rb.rent_status = 'completed'
        AND rb.user_rated = true
        AND rb.owner_rated = true
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

    UPDATE_APPROVED_TO_PICKUP_CONFIRMATION = """
        UPDATE rented_books
        SET
            rent_status = 'awaiting_pickup_confirmation',
            pickup_confirmation_started_at = NOW()
        WHERE rent_status = 'approved'
        AND meetup_date IS NOT NULL
        AND meetup_time IS NOT NULL
        AND (
            -- Use same timezone as cleanup query
            (meetup_date + meetup_time::time) - INTERVAL '1 hour'
            <= (NOW() AT TIME ZONE 'UTC' + INTERVAL '8 hours')
        )
        AND (
            -- Make sure we haven't passed the meetup time yet
            (meetup_date + meetup_time::time)
            >= (NOW() AT TIME ZONE 'UTC' + INTERVAL '8 hours')
        )
        RETURNING rental_id, user_id, book_id, meetup_location;
    """

    UPDATE_ONGOING_TO_RETURN_CONFIRMATION = """
        UPDATE rented_books
        SET
            rent_status = 'awaiting_return_confirmation',
            return_confirmation_started_at = NOW()
        WHERE rent_status = 'ongoing'
        AND rent_end_date IS NOT NULL
        AND meetup_time IS NOT NULL
        AND (
            -- Use same timezone as cleanup query
            (rent_end_date + meetup_time::time) - INTERVAL '1 hour'
            <= (NOW() AT TIME ZONE 'UTC' + INTERVAL '8 hours')
        )
        AND (
            -- Make sure we haven't passed the return time yet
            (rent_end_date + meetup_time::time)
            >= (NOW() AT TIME ZONE 'UTC' + INTERVAL '8 hours')
        )
        RETURNING rental_id, user_id, book_id, meetup_location;
    """

    GET_RENTAL_BY_ID_FULL = """
        SELECT
            rb.rental_id,
            rb.rent_status,
            rb.user_id,
            rb.meetup_time_window,
            rb.total_rent_cost,
            rb.rental_duration_days,
            rb.user_confirmed_pickup,
            rb.owner_confirmed_pickup,
            b.owner_id,
            b.title
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        WHERE rb.rental_id = %s;
    """

    CONFIRM_PICKUP = """
        UPDATE rented_books
        SET
            owner_confirmed_pickup = CASE
                WHEN %s THEN TRUE
                ELSE owner_confirmed_pickup
            END,
            user_confirmed_pickup = CASE
                WHEN %s THEN TRUE
                ELSE user_confirmed_pickup
            END,
            rent_status = CASE
                WHEN (owner_confirmed_pickup OR %s) AND (user_confirmed_pickup OR %s)
                THEN 'ongoing'::rental_status_enum
                ELSE 'awaiting_pickup_confirmation'::rental_status_enum
            END,
            rent_start_date = CASE
                WHEN (owner_confirmed_pickup OR %s) AND (user_confirmed_pickup OR %s)
                THEN CURRENT_DATE
                ELSE rent_start_date
            END,
            rent_end_date = CASE
                WHEN (owner_confirmed_pickup OR %s) AND (user_confirmed_pickup OR %s)
                THEN CURRENT_DATE + (%s || ' days')::interval
                ELSE rent_end_date
            END
        WHERE rental_id = %s
        RETURNING
            rental_id,
            rent_status,
            user_confirmed_pickup,
            owner_confirmed_pickup,
            rent_start_date,
            rent_end_date;
    """

    GET_RENTAL_BY_ID_FULL_RETURN = """
        SELECT
            rb.rental_id,
            rb.rent_status,
            rb.user_id,
            rb.total_rent_cost,
            rb.user_confirmed_return,
            rb.owner_confirmed_return,
            b.owner_id,
            b.title,
            rb.actual_deposit
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        WHERE rb.rental_id = %s;
    """

    CONFIRM_RETURN = """
    UPDATE rented_books rb
    SET
        owner_confirmed_return = CASE
            WHEN %s THEN TRUE
            ELSE owner_confirmed_return
        END,
        user_confirmed_return = CASE
            WHEN %s THEN TRUE
            ELSE user_confirmed_return
        END,
        rent_status = CASE
            WHEN (owner_confirmed_return OR %s) AND (user_confirmed_return OR %s)
            THEN 'completed'::rental_status_enum
            ELSE 'awaiting_return_confirmation'::rental_status_enum
        END
    FROM books b
    WHERE rb.rental_id = %s
    AND rb.book_id = b.book_id
    RETURNING
        rb.rental_id,
        rb.rent_status,
        rb.user_confirmed_return,
        rb.owner_confirmed_return,
        rb.user_id,
        b.owner_id,
        rb.actual_deposit;
"""

    CHECK_BOOK_AVAILABILITY = """
        SELECT
            rb.rental_id,
            rb.rent_status,
            u.username as renter_username
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        JOIN users u ON rb.user_id = u.user_id
        WHERE b.book_id = %s
        AND b.owner_id = %s
        AND rb.rent_status IN ('approved', 'awaiting_pickup_confirmation', 'ongoing', 'awaiting_return_confirmation')
        LIMIT 1;
    """

    GET_BOOK_ID_FROM_RENTAL = """
        SELECT book_id
        FROM rented_books
        WHERE rental_id = %s;
    """
