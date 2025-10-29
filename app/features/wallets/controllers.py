from flask import jsonify, Response

import traceback

from flask_jwt_extended import get_jwt_identity

from .services import WalletServices


class WalletControllers:
    @staticmethod
    def get_current_wallet_balance_controller() -> tuple[Response, int]:
        """Retrieve the current wallet balance of the authenticated user."""

        try:

            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated."}), 401

            current_wallet_balance = WalletServices.get_current_wallet_balance_service(
                user_id
            )

            return jsonify({"currentWalletBalance": current_wallet_balance}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
