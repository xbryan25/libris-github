from flask import request, jsonify, Response

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

    @staticmethod
    def get_reserved_amount_controller() -> tuple[Response, int]:
        """Retrieve the reserved amount balance of the authenticated user."""

        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated."}), 401

            reserved_wallet_balance = WalletServices.get_reserved_amount_service(
                user_id
            )

            return jsonify({"reservedamount": reserved_wallet_balance}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_reserved_amount_controller() -> tuple[Response, int]:
        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated."}), 401

            update_details = request.get_json()

            amount_to_reserve = float(update_details.get("amount_to_reserve", 0))

            success = WalletServices.update_reserved_amount_service(
                user_id, amount_to_reserve
            )

            if success:
                return (
                    jsonify({"message": "Reserved amount updated successfully."}),
                    200,
                )
            else:
                return (
                    jsonify({"message": "Failed to update reserved amount."}),
                    400,
                )

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def buy_readits_controller() -> tuple[Response, int]:
        """(add later)"""

        packs_to_readits_dict = {
            "starter": {"amount": 100, "readits": 200},
            "popular": {"amount": 150, "readits": 600},
            "pro": {"amount": 350, "readits": 1000},
            "ultra": {"amount": 750, "readits": 5000},
        }

        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated."}), 401

            purchase_details = request.get_json()

            selectedPack = purchase_details.get("selectedPack")

            amount_needed_in_pack = float(
                packs_to_readits_dict.get(selectedPack, {"amount": 0})["amount"]
            )  # price of pack
            readits_from_pack = float(
                packs_to_readits_dict.get(selectedPack, {"readits": 200})["readits"]
            )

            invoice_url = WalletServices.buy_readits_service(
                user_id, amount_needed_in_pack, readits_from_pack
            )

            return (
                jsonify({"invoiceUrl": invoice_url}),
                200,
            )
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
