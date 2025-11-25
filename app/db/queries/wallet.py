class WalletQueries:
    INCREMENT_WALLET_BALANCE = "UPDATE readits_wallets SET balance = balance + %s, last_updated = %s WHERE user_id = %s"

    INSERT_TRANSACTION_USING_USER_ID = """
        INSERT INTO transactions (
            wallet_id,
            amount,
            transaction_date,
            type
        )
        SELECT
            rw.wallet_id,
            %s AS amount,
            %s AS transaction_date,
            %s AS type
        FROM readits_wallets rw
        INNER JOIN users u ON rw.user_id = u.user_id
        WHERE u.user_id = %s;
    """

    DEDUCT_FROM_RESERVED_AND_BALANCE = """
        UPDATE readits_wallets
        SET
            reserved_amount = reserved_amount - %s,
            balance = balance - %s,
            last_updated = %s
        WHERE user_id = %s
        AND reserved_amount >= %s
        AND balance >= %s
        RETURNING wallet_id, balance, reserved_amount;
    """

    INSERT_TRANSACTION_USING_WALLET_ID = """
        INSERT INTO transactions (
            wallet_id,
            amount,
            transaction_date,
            type
        )
        VALUES (%s, %s, %s, %s)
        RETURNING transaction_id;
    """

    GET_WALLET_ID_BY_USER_ID = """
        SELECT wallet_id
        FROM readits_wallets
        WHERE user_id = %s;
    """
