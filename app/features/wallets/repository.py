from app.db.queries import CommonQueries, WalletQueries

from flask import current_app


class WalletRepository:
    @staticmethod
    def get_current_wallet_balance(user_id) -> dict[str, int]:
        """
        Retrieve the current wallet balance of the authenticated user.

        Args:
            user_id (str): The user_id of the authenticated user.

        Returns:
             dict: A dictionary containing the current wallet balance of the authenticated user.
        """

        db = current_app.extensions["db"]

        return db.fetch_one(
            CommonQueries.GET_COLUMN_BY_FIELD.format(
                column="balance", table="readits_wallets", field="user_id"
            ),
            (user_id,),
        )

    @staticmethod
    def add_readits_to_wallet_from_paid_invoice(user_id, readits_to_add, last_updated):

        db = current_app.extensions["db"]

        return db.execute_query(
            WalletQueries.INCREMENT_WALLET_BALANCE,
            (readits_to_add, last_updated, user_id),
        )

    @staticmethod
    def add_transaction(
        readits_transaction_amount, transaction_date, transaction_type, user_id
    ):

        db = current_app.extensions["db"]

        return db.execute_query(
            WalletQueries.INSERT_TRANSACTION_USING_USER_ID,
            (readits_transaction_amount, transaction_date, transaction_type, user_id),
        )
