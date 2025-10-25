class UserQueries:
    GET_PROFILE_INFO = (
        "SELECT u.username, u.first_name, u.middle_name, u.last_name, u.date_of_birth, "
        "u.phone_number, u.account_activated_at, u.trust_score, u.profile_image_url, "
        "a.country, a.city, a.barangay, a.street, a.postal_code "
        "FROM users u "
        "JOIN user_address a ON u.user_id = a.user_id "
        "WHERE u.user_id = %s"
    )
    GET_USER_ADDRESS = "SELECT country, city, barangay, street, postal_code FROM user_address WHERE user_id = %s LIMIT 1"
    GET_TRUST_SCORE_STATS = (
        "SELECT AVG(trust_score) as average_trust_score, COUNT(*) as total_users "
        "FROM users WHERE trust_score IS NOT NULL"
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
