from flask import Blueprint, Response
from .controllers import WalletControllers

from flask_jwt_extended import jwt_required

wallets_bp = Blueprint("wallets_bp", __name__)


@wallets_bp.route("/get-current-balance", methods=["GET"])
@jwt_required()
def get_current_wallet_balance() -> tuple[Response, int]:
    """
    Retrieve the current wallet balance of the authenticated user.

    This endpoint requires a valid access token (sent via an HTTP-only cookie).
    It returns the wallet balance associated with the authenticated user.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        currentWalletBalance: The current wallet balance of a user.

    Possible errors:

        401 if the user is not authenticated or the token is missing/invalid.

        500 if an unexpected error occurs during processing.
    """

    return WalletControllers.get_current_wallet_balance_controller()


@wallets_bp.route("/get-reserved-amount", methods=["GET"])
@jwt_required()
def get_reserved_amount() -> tuple[Response, int]:
    """
    Retrieve the reserved amount amount of the authenticated user.

    This endpoint requires a valid access token (sent via an HTTP-only cookie).
    It returns the reserved amount amount associated with the authenticated user.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        reservedamounte: The reserved amount of a user.

    Possible errors:

        401 if the user is not authenticated or the token is missing/invalid.

        500 if an unexpected error occurs during processing.
    """

    return WalletControllers.get_reserved_amount_controller()


@wallets_bp.route("/update-reserved-amount", methods=["PATCH"])
@jwt_required()
def update_reserved_amount() -> tuple[Response, int]:
    """
    Updates the reserved amount of the authenticated user.

    This endpoint requires a valid access token (sent via an HTTP-only cookie).
    It updates the reserved amount associated with the authenticated user.

    Request body:
        - amount: The new reserved amount to set (float).

    Response JSON:
        reservedAmount: The updated reserved amount of the user.

    Possible errors:

        400 if the request body is missing or invalid.

        401 if the user is not authenticated or the token is missing/invalid.
    """
    return WalletControllers.update_reserved_amount_controller()


@wallets_bp.route("/buy-readits", methods=["POST"])
@jwt_required()
def buy_readits() -> tuple[Response, int]:
    """
    (add later)
    """
    return WalletControllers.buy_readits_controller()
