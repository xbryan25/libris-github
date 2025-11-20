class RentalsQueries:
    INSERT_RENTAL = """
        INSERT INTO rented_books (
            rental_id,
            user_id,
            book_id,
            rent_status,
            reserved_at,
            reservation_expires_at,
            total_rent_cost,
            rental_duration_days,
            all_fees_captured,
            meetup_time_window,
            meetup_location,
            meetup_date
        )
        VALUES (
            gen_random_uuid(),
            %s,  -- user_id
            %s,  -- book_id
            'pending',  -- rent_status
            %s,  -- reserved_at
            %s,  -- reservation_expires_at
            %s,  -- total_rent_cost
            %s,  -- rental_duration_days
            false,  -- all_fees_captured
            %s,  -- meetup_time_window
            %s,  -- meetup_location
            %s   -- meetup_date
        )
        RETURNING rental_id;
    """
