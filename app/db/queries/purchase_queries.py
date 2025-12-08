class PurchasesQueries:
    INSERT_PURCHASE = """
        INSERT INTO purchased_books (
            purchase_id,
            user_id,
            book_id,
            original_owner_id,
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
            (SELECT owner_id FROM books WHERE book_id = %s),
            'pending',
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

    GET_USER_PURCHASES_WITH_STATUS = """
        SELECT
            pb.purchase_id,
            pb.purchase_status,
            pb.original_owner_id,
            pb.user_id,
            b.book_id,
            b.title,
            b.author,
            bi.image_url AS image,
            u.username AS "from",
            pb.all_fees_captured,
            pb.reserved_at,
            pb.reservation_expires_at,
            pb.meetup_location,
            pb.meetup_time_window,
            pb.meetup_time,
            pb.meetup_date,
            pb.pickup_confirmation_started_at,
            pb.user_confirmed_pickup,
            pb.owner_confirmed_pickup,
            pb.user_rated,
            pb.owner_rated,
            pb.total_buy_cost AS cost,
            pb.transfer_decision_pending,
            pb.ownership_transferred
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        JOIN users u ON pb.original_owner_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE pb.user_id = %s
        AND (
            pb.purchase_status IN ('pending', 'approved', 'awaiting_pickup_confirmation')
            OR (pb.purchase_status = 'completed' AND pb.transfer_decision_pending = TRUE)
            OR (pb.purchase_status = 'completed' AND pb.user_rated = FALSE)
        );
    """

    GET_COMPLETED_PURCHASE = """
        SELECT
            pb.purchase_id,
            pb.purchase_status,
            pb.original_owner_id,
            pb.user_id,
            b.book_id,
            b.title,
            b.author,
            bi.image_url AS image,
            u.username AS "from",
            pb.all_fees_captured,
            pb.reserved_at,
            pb.reservation_expires_at,
            pb.meetup_location,
            pb.meetup_time_window,
            pb.meetup_time,
            pb.meetup_date,
            pb.pickup_confirmation_started_at,
            pb.user_confirmed_pickup,
            pb.owner_confirmed_pickup,
            pb.user_rated,
            pb.owner_rated,
            pb.total_buy_cost AS cost,
            pb.transfer_decision_pending,
            pb.ownership_transferred
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        JOIN users u ON pb.original_owner_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE pb.purchase_id = %s
        AND pb.user_id = %s
        AND pb.purchase_status = 'completed'
        AND pb.user_rated = true
        AND pb.owner_rated = true
    """

    GET_USER_COMPLETED_PURCHASES = """
        SELECT
            pb.purchase_id,
            pb.purchase_status,
            pb.original_owner_id,
            pb.user_id,
            b.book_id,
            b.title,
            b.author,
            bi.image_url AS image,
            u.username AS "from",
            pb.all_fees_captured,
            pb.reserved_at,
            pb.reservation_expires_at,
            pb.meetup_location,
            pb.meetup_time_window,
            pb.meetup_time,
            pb.meetup_date,
            pb.pickup_confirmation_started_at,
            pb.user_confirmed_pickup,
            pb.owner_confirmed_pickup,
            pb.user_rated,
            pb.owner_rated,
            pb.total_buy_cost AS cost,
            pb.transfer_decision_pending,
            pb.ownership_transferred
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        JOIN users u ON pb.original_owner_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE pb.user_id = %s
        AND pb.purchase_status = 'completed'
        AND pb.user_rated = true
        AND pb.owner_rated = true
        ORDER BY meetup_date {sort_order}
        LIMIT %s OFFSET %s
    """

    GET_USER_COMPLETED_PURCHASES_COUNT = """
        SELECT COUNT(*) AS count
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        JOIN users u ON pb.original_owner_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE pb.user_id = %s
        AND pb.purchase_status = 'completed'
        AND pb.user_rated = true
        AND pb.owner_rated = true
    """

    GET_USER_SALES_WITH_STATUS = """
        SELECT
            pb.purchase_id,
            pb.purchase_status,
            pb.original_owner_id,
            pb.user_id,
            b.book_id,
            b.title,
            b.author,
            bi.image_url AS image,
            u.username AS "to",
            pb.all_fees_captured,
            pb.reserved_at,
            pb.reservation_expires_at,
            pb.meetup_date,
            pb.meetup_location,
            pb.meetup_time_window,
            pb.meetup_time,
            pb.pickup_confirmation_started_at,
            pb.user_confirmed_pickup,
            pb.owner_confirmed_pickup,
            pb.user_rated,
            pb.owner_rated,
            pb.total_buy_cost AS cost,
            pb.transfer_decision_pending,
            pb.ownership_transferred
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        JOIN users u ON pb.user_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE pb.original_owner_id = %s
        AND (
            pb.purchase_status IN ('pending', 'approved', 'awaiting_pickup_confirmation')
            OR (pb.purchase_status = 'completed' AND pb.owner_rated = FALSE)
        );
    """

    GET_COMPLETED_SALE = """
        SELECT
            pb.purchase_id,
            pb.purchase_status,
            pb.original_owner_id,
            pb.user_id,
            b.book_id,
            b.title,
            b.author,
            bi.image_url AS image,
            u.username AS "to",
            pb.all_fees_captured,
            pb.reserved_at,
            pb.reservation_expires_at,
            pb.meetup_location,
            pb.meetup_time_window,
            pb.meetup_time,
            pb.meetup_date,
            pb.pickup_confirmation_started_at,
            pb.user_confirmed_pickup,
            pb.owner_confirmed_pickup,
            pb.user_rated,
            pb.owner_rated,
            pb.total_buy_cost AS cost,
            pb.transfer_decision_pending,
            pb.ownership_transferred
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        JOIN users u ON pb.user_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE pb.purchase_id = %s
        AND pb.original_owner_id = %s
        AND pb.purchase_status = 'completed'
        AND pb.user_rated = true
        AND pb.owner_rated = true
    """

    GET_USER_COMPLETED_SALES = """
        SELECT
            pb.purchase_id,
            pb.purchase_status,
            pb.original_owner_id,
            pb.user_id,
            b.book_id,
            b.title,
            b.author,
            bi.image_url AS image,
            u.username AS "to",
            pb.all_fees_captured,
            pb.reserved_at,
            pb.reservation_expires_at,
            pb.meetup_location,
            pb.meetup_time_window,
            pb.meetup_time,
            pb.meetup_date,
            pb.pickup_confirmation_started_at,
            pb.user_confirmed_pickup,
            pb.owner_confirmed_pickup,
            pb.user_rated,
            pb.owner_rated,
            pb.total_buy_cost AS cost,
            pb.transfer_decision_pending,
            pb.ownership_transferred
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        JOIN users u ON pb.user_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE pb.original_owner_id = %s
        AND pb.purchase_status = 'completed'
        AND pb.user_rated = true
        AND pb.owner_rated = true
        ORDER BY meetup_date {sort_order}
        LIMIT %s OFFSET %s
    """

    GET_USER_COMPLETED_SALES_COUNT = """
        SELECT COUNT(*) AS count
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        JOIN users u ON pb.user_id = u.user_id
        LEFT JOIN book_images bi ON b.book_id = bi.book_id AND bi.order_num = 1
        WHERE pb.original_owner_id = %s
        AND pb.purchase_status = 'completed'
        AND pb.user_rated = true
        AND pb.owner_rated = true
    """

    APPROVE_PURCHASE = """
        UPDATE purchased_books
        SET
            purchase_status = 'approved',
            meetup_time = %s,
            all_fees_captured = TRUE
        WHERE purchase_id = %s
        AND purchase_status = 'pending'
        RETURNING purchase_id, purchase_status, meetup_time, all_fees_captured;
    """

    GET_PURCHASE_BY_ID = """
        SELECT
            pb.purchase_id,
            pb.purchase_status,
            pb.user_id,
            pb.meetup_time_window,
            pb.total_buy_cost,
            pb.original_owner_id,  -- ADDED
            b.owner_id as current_owner_id,  -- RENAMED for clarity
            b.title
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        WHERE pb.purchase_id = %s;
    """

    DELETE_PURCHASE = """
    DELETE FROM purchased_books
    WHERE purchase_id = %s
    AND purchase_status = 'pending'
    RETURNING purchase_id;
    """

    UPDATE_APPROVED_TO_PICKUP_CONFIRMATION = """
        UPDATE purchased_books
        SET
            purchase_status = 'awaiting_pickup_confirmation',
            pickup_confirmation_started_at = NOW()
        WHERE purchase_status = 'approved'
        AND meetup_date IS NOT NULL
        AND meetup_time IS NOT NULL
        AND (
            (meetup_date + meetup_time::time) - INTERVAL '1 hour'
            <= (NOW() AT TIME ZONE 'UTC' + INTERVAL '8 hours')
        )
        AND (
            (meetup_date + meetup_time::time)
            >= (NOW() AT TIME ZONE 'UTC' + INTERVAL '8 hours')
        )
        RETURNING purchase_id, user_id, book_id, meetup_location;
    """

    GET_PURCHASE_BY_ID_FULL = """
        SELECT
            pb.purchase_id,
            pb.purchase_status,
            pb.user_id,
            pb.meetup_time_window,
            pb.total_buy_cost,
            pb.user_confirmed_pickup,
            pb.owner_confirmed_pickup,
            pb.original_owner_id,
            b.owner_id as current_owner_id,
            b.title
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        WHERE pb.purchase_id = %s;
    """

    CONFIRM_PICKUP = """
        UPDATE purchased_books
        SET
            owner_confirmed_pickup = CASE
                WHEN %s THEN TRUE
                ELSE owner_confirmed_pickup
            END,
            user_confirmed_pickup = CASE
                WHEN %s THEN TRUE
                ELSE user_confirmed_pickup
            END,
            purchase_status = CASE
                WHEN (owner_confirmed_pickup OR %s) AND (user_confirmed_pickup OR %s)
                THEN 'completed'::purchase_status_enum
                ELSE 'awaiting_pickup_confirmation'::purchase_status_enum
            END,
            transfer_decision_pending = CASE
                WHEN (owner_confirmed_pickup OR %s) AND (user_confirmed_pickup OR %s)
                THEN TRUE
                ELSE transfer_decision_pending
            END
        WHERE purchase_id = %s
        RETURNING
            purchase_id,
            purchase_status,
            user_confirmed_pickup,
            owner_confirmed_pickup,
            transfer_decision_pending;
    """

    SUBMIT_TRANSFER_DECISION = """
        UPDATE purchased_books
        SET
            ownership_transferred = %s,
            transfer_decision_pending = FALSE
        WHERE purchase_id = %s
        AND purchase_status = 'completed'
        AND transfer_decision_pending = TRUE
        RETURNING
            purchase_id,
            purchase_status,
            ownership_transferred,
            transfer_decision_pending,
            user_id,
            book_id;
    """

    GET_PURCHASE_WITH_BOOK_DETAILS = """
        SELECT
            pb.purchase_id,
            pb.user_id,
            pb.book_id,
            pb.ownership_transferred,
            pb.transfer_decision_pending,
            pb.original_owner_id,
            b.owner_id as current_owner_id,
            b.title
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        WHERE pb.purchase_id = %s;
    """

    CHECK_BOOK_AVAILABILITY = """
        SELECT
            pb.purchase_id,
            pb.purchase_status,
            u.username as buyer_username
        FROM purchased_books pb
        JOIN books b ON pb.book_id = b.book_id
        JOIN users u ON pb.user_id = u.user_id
        WHERE b.book_id = %s
        AND pb.original_owner_id = %s
        AND pb.purchase_status IN ('approved', 'awaiting_pickup_confirmation')
        LIMIT 1;
    """

    GET_BOOK_ID_FROM_PURCHASE = """
        SELECT book_id
        FROM purchased_books
        WHERE purchase_id = %s;
    """

    PROCESS_TRANSFER_DECISION_YES = """
        WITH updated_purchase AS (
            UPDATE purchased_books
            SET
                ownership_transferred = TRUE,
                transfer_decision_pending = FALSE
            WHERE purchase_id = %s
            AND purchase_status = 'completed'
            AND transfer_decision_pending = TRUE
            RETURNING book_id, user_id
        )
        UPDATE books
        SET owner_id = (SELECT user_id FROM updated_purchase)
        WHERE book_id = (SELECT book_id FROM updated_purchase)
        RETURNING book_id, owner_id;
    """

    PROCESS_TRANSFER_DECISION_NO = """
        WITH updated_purchase AS (
            UPDATE purchased_books
            SET
                ownership_transferred = FALSE,
                transfer_decision_pending = FALSE
            WHERE purchase_id = %s
            AND purchase_status = 'completed'
            AND transfer_decision_pending = TRUE
            RETURNING book_id
        )
        UPDATE books
        SET is_soft_deleted = TRUE
        WHERE book_id = (SELECT book_id FROM updated_purchase)
        RETURNING book_id, is_soft_deleted;
    """
