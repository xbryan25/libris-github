class RatingQueries:

    INSERT_RATING = """
        INSERT INTO user_ratings (rater_id, rated_user_id, score, comment, rental_id, purchase_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING rating_id
    """

    CHECK_EXISTING_RATING = """
        SELECT EXISTS(
            SELECT 1 FROM user_ratings r
            WHERE r.rental_id = %s
            AND r.rater_id = %s
        ) as exists
    """

    CHECK_EXISTING_RATING_PURCHASE = """
        SELECT EXISTS(
            SELECT 1 FROM user_ratings r
            WHERE r.purchase_id = %s
            AND r.rater_id = %s
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
    UPDATE_USER_TRUST_SCORE = (
        "UPDATE users SET trust_score = %s WHERE user_id = %s RETURNING trust_score"
    )
    UPDATE_PURCHASE_USER_RATED_FLAG = """
        UPDATE purchased_books
        SET user_rated = TRUE
        WHERE purchase_id = %s
        RETURNING purchase_id
    """

    UPDATE_PURCHASE_OWNER_RATED_FLAG = """
        UPDATE purchased_books
        SET owner_rated = TRUE
        WHERE purchase_id = %s
        RETURNING purchase_id
    """

    GET_PURCHASE_INFO = """
        SELECT
            pb.purchase_id,
            pb.user_id,
            pb.original_owner_id as owner_id,
            pb.purchase_status,
            pb.user_rated,
            pb.owner_rated
        FROM purchased_books pb
        WHERE pb.purchase_id = %s
    """

    GET_RATINGS_FROM_PURCHASE_FROM_RATER = """
        SELECT
            score AS given_rating,
            comment AS given_comment
        FROM user_ratings
        WHERE purchase_id = %s AND rater_id = %s
    """

    GET_RATINGS_FROM_PURCHASE_FROM_RATED_USER = """
        SELECT
            score AS received_rating,
            comment AS received_comment
        FROM user_ratings
        WHERE purchase_id = %s AND rated_user_id = %s
    """
