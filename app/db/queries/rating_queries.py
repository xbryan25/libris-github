class RatingQueries:

    INSERT_RATING = """
        INSERT INTO user_ratings (rater_id, rated_user_id, score, comment)
        VALUES (%s, %s, %s, %s)
        RETURNING rating_id
    """

    CHECK_EXISTING_RATING = """
        SELECT EXISTS(
            SELECT 1 FROM user_ratings r
            JOIN rented_books rb ON (
                (r.rater_id = rb.user_id AND r.rated_user_id = (SELECT owner_id FROM books WHERE book_id = rb.book_id))
                OR
                (r.rater_id = (SELECT owner_id FROM books WHERE book_id = rb.book_id) AND r.rated_user_id = rb.user_id)
            )
            WHERE rb.rental_id = %s AND r.rater_id = %s
        ) as exists
    """

    GET_USER_RATINGS = """
        SELECT
            r.rating_id,
            r.score as rating,
            r.comment as review,
            u.username as rater_username,
            u.profile_image_url as rater_profile_image
        FROM user_ratings r
        JOIN users u ON r.rater_id = u.user_id
        WHERE r.rated_user_id = %s
        ORDER BY r.rating_id DESC
    """

    UPDATE_USER_RATED_FLAG = """
        UPDATE rented_books
        SET user_rated = TRUE
        WHERE rental_id = %s
        RETURNING rental_id
    """

    UPDATE_OWNER_RATED_FLAG = """
        UPDATE rented_books
        SET owner_rated = TRUE
        WHERE rental_id = %s
        RETURNING rental_id
    """

    GET_RENTAL_INFO = """
        SELECT
            rb.rental_id,
            rb.user_id,
            b.owner_id,
            rb.rent_status,
            rb.user_rated,
            rb.owner_rated
        FROM rented_books rb
        JOIN books b ON rb.book_id = b.book_id
        WHERE rb.rental_id = %s
    """

    UPDATE_USER_TRUST_SCORE = "UPDATE users SET trust_score = %s WHERE user_id = %s"
