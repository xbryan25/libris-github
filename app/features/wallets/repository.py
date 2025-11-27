from app.db.queries import CommonQueries, WalletQueries
from datetime import datetime
from flask import current_app
from typing import Any


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
    def get_reserved_amount(user_id) -> dict[str, int]:
        """
        Retrieve the reserved amount of the authenticated user.

        Args:
            user_id (str): The user_id of the authenticated user.

        Returns:
             dict: A dictionary containing the reserved amount of the authenticated user.
        """

        db = current_app.extensions["db"]

        return db.fetch_one(
            CommonQueries.GET_COLUMN_BY_FIELD.format(
                column="reserved_amount", table="readits_wallets", field="user_id"
            ),
            (user_id,),
        )

    @staticmethod
    def update_reserved_amount(user_id: str, new_reserved_amount: float) -> bool:
        """
        Update the reserved amount of the authenticated user.

        Args:
            user_id (str): The user_id of the authenticated user.
            new_reserved_amount (float): The new total reserved amount to set.

        Returns:
            bool: True if the update was successful, False otherwise.
        """

        db = current_app.extensions["db"]

        try:
            db.execute_query(
                WalletQueries.UPDATE_RESERVED_AMOUNT,
                (new_reserved_amount, user_id),
            )
            return True
        except Exception as e:
            print(f"DB Error: {e}")
            return False

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

    @staticmethod
    def deduct_from_reserved_and_balance(user_id: str, amount: int) -> dict | None:
        """
        Deduct amount from both reserved_amount and balance.

        Args:
            user_id: The user's ID
            amount: Amount to deduct from both reserved and balance

        Returns:
            dict with wallet_id, balance, reserved_amount or None if insufficient funds
        """
        db = current_app.extensions["db"]
        last_updated = datetime.now()

        result = db.fetch_one(
            WalletQueries.DEDUCT_FROM_RESERVED_AND_BALANCE,
            (amount, amount, last_updated, user_id, amount, amount),
        )

        return result

    @staticmethod
    def get_wallet_id_by_user_id(user_id: str) -> str | None:
        """Get wallet_id for a given user_id."""
        db = current_app.extensions["db"]

        result = db.fetch_one(WalletQueries.GET_WALLET_ID_BY_USER_ID, (user_id,))

        return result.get("wallet_id") if result else None

    @staticmethod
    def insert_transaction(
        wallet_id: str, amount: int, transaction_type: str
    ) -> dict | None:
        """
        Insert a transaction record.

        Args:
            wallet_id: The wallet ID
            amount: Transaction amount (positive for credit, negative for debit)
            transaction_type: Type of transaction (rent, purchase, topup, etc.)

        Returns:
            dict with transaction_id or None if failed
        """
        db = current_app.extensions["db"]
        transaction_date = datetime.now()

        result = db.fetch_one(
            WalletQueries.INSERT_TRANSACTION_USING_WALLET_ID,
            (wallet_id, amount, transaction_date, transaction_type),
        )

        return result

    @staticmethod
    def deduct_from_reserved_amount(user_id: str, amount: int) -> dict | None:
        """
        Deduct amount from reserved_amount only (release reserved funds).

        Args:
            user_id: The user's ID
            amount: Amount to deduct from reserved_amount

        Returns:
            dict with wallet_id, balance, reserved_amount or None if insufficient reserved funds
        """
        db = current_app.extensions["db"]
        last_updated = datetime.now()

        result = db.fetch_one(
            WalletQueries.DEDUCT_FROM_RESERVED_AMOUNT,
            (amount, last_updated, user_id, amount),
        )

        return result

    @staticmethod
    def return_security_deposit(
        renter_user_id: str, owner_user_id: str, deposit_amount: int
    ) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        """
        Return security deposit from owner to renter.
        Deducts from owner's wallet and adds to renter's wallet.

        Args:
            renter_user_id: The renter's user ID
            owner_user_id: The owner's user ID
            deposit_amount: The security deposit amount to return

        Returns:
            tuple: (renter_wallet_result, owner_wallet_result) or (None, None) if failed
        """

        db = current_app.extensions["db"]
        now = datetime.now()

        # Add to renter's wallet
        renter_params = (deposit_amount, now, renter_user_id)
        renter_result = db.fetch_one(
            WalletQueries.RETURN_SECURITY_DEPOSIT_TO_RENTER, renter_params
        )

        if not renter_result:
            return None, None

        # Deduct from owner's wallet
        owner_params = (deposit_amount, now, owner_user_id, deposit_amount)
        owner_result = db.fetch_one(
            WalletQueries.DEDUCT_SECURITY_DEPOSIT_FROM_OWNER, owner_params
        )

        if not owner_result:
            # Rollback renter's wallet if owner doesn't have sufficient funds
            rollback_params = (deposit_amount, now, renter_user_id)
            db.fetch_one(
                """
                UPDATE readits_wallets
                SET
                    balance = balance - %s,
                    last_updated = %s
                WHERE user_id = %s
                RETURNING wallet_id;
                """,
                rollback_params,
            )
            return None, None

        return renter_result, owner_result

    @staticmethod
    def insert_deposit_transaction(
        wallet_id: str, amount: int, transaction_type: str
    ) -> dict[str, Any] | None:
        """
        Create a transaction log for deposit return/received.

        Args:
            wallet_id: The wallet ID
            amount: The transaction amount (positive for renter, negative for owner)
            transaction_type: Either 'deposit_received' or 'deposit_returned'

        Returns:
            dict with transaction details or None if failed
        """
        from app.db.queries.wallet import WalletQueries
        from datetime import datetime

        db = current_app.extensions["db"]
        now = datetime.now()

        params = (wallet_id, amount, now, transaction_type)
        result = db.fetch_one(WalletQueries.INSERT_DEPOSIT_TRANSACTION, params)

        return result

    @staticmethod
    def add_rental_fee_to_owner(
        owner_user_id: str, amount: int
    ) -> dict[str, Any] | None:
        """
        Add rental fee to owner's wallet balance.

        Args:
            owner_user_id: The owner's user ID
            amount: The rental fee amount to add

        Returns:
            dict with wallet_id, balance, user_id or None if failed
        """
        db = current_app.extensions["db"]
        now = datetime.now()

        params = (amount, now, owner_user_id)
        result = db.fetch_one(WalletQueries.ADD_RENTAL_FEE_TO_OWNER, params)

        return result
