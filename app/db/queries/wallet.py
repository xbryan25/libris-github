class WalletQueries:
    INCREMENT_WALLET_BALANCE = "UPDATE readits_wallets SET balance = balance + %s, last_updated = %s WHERE user_id = %s"
