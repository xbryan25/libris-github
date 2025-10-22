class DashboardQueries:
    DASHBOARD_COUNTS = """
            SELECT
            (SELECT COUNT(*) FROM rented_books WHERE user_id = %s) AS books_borrowed,
            (SELECT COUNT(*)
                FROM rented_books rb
                JOIN books b ON rb.book_id = b.book_id
                WHERE b.owner_id = %s AND rb.user_id != %s AND rb.rent_status = 'ongoing') AS currently_lending,
            (SELECT COUNT(*) FROM rented_books WHERE user_id = %s AND rent_status = 'ongoing') AS currently_renting,
            (SELECT COUNT(*)
                FROM purchased_books pb
                JOIN books b ON pb.book_id = b.book_id
                WHERE b.owner_id = %s AND pb.user_id != %s AND pb.purchase_status = 'completed') AS books_sold,
            (SELECT COUNT(*) FROM purchased_books WHERE user_id = %s AND purchase_status = 'completed') AS books_bought,
            (
                COALESCE(
                (SELECT SUM(rb.total_rent_cost)
                FROM rented_books rb
                JOIN books b ON rb.book_id = b.book_id
                WHERE b.owner_id = %s
                AND rb.user_id != %s
                AND rb.rent_status = 'completed'),
                0
                )
                +
                COALESCE(
                (SELECT SUM(pb.total_buy_cost)
                FROM purchased_books pb
                JOIN books b ON pb.book_id = b.book_id
                WHERE b.owner_id = %s
                AND pb.user_id != %s
                AND pb.purchase_status = 'completed'),
                0
                )
            ) AS total_earnings
            """
