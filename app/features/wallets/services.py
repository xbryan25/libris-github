from .repository import WalletRepository


class WalletServices:
    @staticmethod
    def get_current_wallet_balance_service(user_id) -> int:
        """
        Retrieve the current wallet balance of the authenticated user.

        Args:
            user_id (str): The user_id of the authenticated user.

        Returns:
            int: The current wallet balance of the authenticated user.
        """

        return WalletRepository.get_current_wallet_balance(user_id)["balance"]
