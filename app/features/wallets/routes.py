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
