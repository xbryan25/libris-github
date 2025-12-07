class DashboardQueries:
    DASHBOARD_COUNTS = """
        SELECT
            (SELECT COUNT(*)
             FROM rented_books
             WHERE user_id = %s
             AND rent_status = 'completed') AS books_borrowed,
            (SELECT COUNT(*)
             FROM rented_books rb
             JOIN books b ON rb.book_id = b.book_id
             WHERE b.owner_id = %s
             AND rb.user_id != %s
             AND rb.rent_status = 'ongoing') AS currently_lending,
            (SELECT COUNT(*)
             FROM rented_books
             WHERE user_id = %s
             AND rent_status = 'ongoing') AS currently_renting,
            (SELECT COUNT(*)
             FROM purchased_books pb
             WHERE pb.original_owner_id = %s
             AND pb.user_id != %s
             AND pb.purchase_status = 'completed') AS books_sold,
            (SELECT COUNT(*)
             FROM purchased_books
             WHERE user_id = %s
             AND purchase_status = 'completed') AS books_bought,
            -- Total earnings: from rentals + sales where you were the original owner
            (
                -- Earnings from rentals (use actual_rate, not total_rent_cost which includes deposit)
                COALESCE(
                    (SELECT SUM(rb.actual_rate * rb.rental_duration_days)
                     FROM rented_books rb
                     WHERE rb.original_owner_id = %s
                     AND rb.user_id != %s
                     AND rb.rent_status = 'completed'),
                    0
                )
                +
                -- Earnings from sales
                COALESCE(
                    (SELECT SUM(pb.total_buy_cost)
                     FROM purchased_books pb
                     WHERE pb.original_owner_id = %s
                     AND pb.user_id != %s
                     AND pb.purchase_status = 'completed'
                     AND pb.ownership_transferred = TRUE),
                    0
                )
            ) AS total_earnings
    """
