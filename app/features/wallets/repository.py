from app.db.queries import CommonQueries

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
