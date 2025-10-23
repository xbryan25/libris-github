class UserQueries:
    GET_PROFILE_INFO = (
        "SELECT u.username, u.first_name, u.middle_name, u.last_name, u.date_of_birth, "
        "u.phone_number, u.account_activated_at, "
        "a.country, a.city, a.barangay, a.street, a.postal_code "
        "FROM users u "
        "JOIN user_address a ON u.user_id = a.user_id "
        "WHERE u.user_id = %s"
    )
    GET_USER_ADDRESS = "SELECT country, city, barangay, street, postal_code FROM user_addresses WHERE user_id = %s LIMIT 1"
