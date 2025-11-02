class UserQueries:
    GET_PROFILE_INFO = (
        "SELECT u.username, u.first_name, u.middle_name, u.last_name, u.date_of_birth, "
        "u.phone_number, u.account_activated_at, u.trust_score, u.profile_image_url, "
        "a.country, a.city, a.barangay, a.street, a.postal_code "
        "FROM users u "
        "LEFT JOIN user_address a ON u.user_id = a.user_id "
        "WHERE u.user_id = %s"
    )
    GET_USER_ADDRESS = "SELECT country, city, barangay, street, postal_code FROM user_address WHERE user_id = %s LIMIT 1"
    GET_TRUST_SCORE_PERCENTILE = (
        "SELECT * FROM ( "
        "    SELECT "
        "        u.user_id, "
        "        100.0 * cume_dist() OVER (ORDER BY trust_score) AS trust_score_percentile "
        "    FROM users u "
        ") sub "
        "WHERE user_id::text = %s"
    )

    UPDATE_USER_PROFILE = (
        "UPDATE users SET first_name = %s, middle_name = %s, last_name = %s, "
        "date_of_birth = %s, phone_number = %s, profile_image_url = %s WHERE user_id = %s"
    )
    UPDATE_USER_ADDRESS = (
        "UPDATE user_address SET country = %s, city = %s, barangay = %s, "
        "street = %s, postal_code = %s WHERE user_id = %s"
    )
    GET_USER_PROFILE = (
        "SELECT first_name, middle_name, last_name, date_of_birth, phone_number, profile_image_url "
        "FROM users WHERE user_id = %s"
    )
    GET_LIBRARY_DETAILS = """
            SELECT
                (
                    SELECT COUNT(*)
                    FROM books AS b
                    LEFT JOIN purchased_books AS p ON b.book_id = p.book_id
                    WHERE b.owner_id = %s
                    AND (p.purchase_status IS NULL OR p.purchase_status != 'completed')
                ) AS books_owned,

                (
                    SELECT COUNT(*)
                    FROM rented_books AS r
                    WHERE r.user_id = %s
                ) AS books_rented,

                (
                    SELECT COUNT(*)
                    FROM purchased_books AS p2
                    WHERE p2.user_id = %s
                    AND p2.purchase_status = 'completed'
                ) AS books_bought
        """
