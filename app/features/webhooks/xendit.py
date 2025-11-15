from flask import Blueprint, request, jsonify, current_app

from app.features.wallets.services import WalletServices

webhooks_bp = Blueprint("webhooks", __name__)


@webhooks_bp.route("/xendit", methods=["POST"])
def handle_xendit_webhook():

    callback_token = request.headers.get("X-Callback-Token")

    if not callback_token:
        return jsonify({"error": "Missing callback token"}), 400

    secret_key = current_app.config["XENDIT_WEBHOOK_SECRET_KEY"]

    # Verify if X-Callback-Token is the same as webhook secret key
    if callback_token != secret_key:
        return jsonify({"error": "Invalid callback token"}), 401

    data = request.json
    status = (data or {}).get("status")

    if status == "PAID":
        return handle_invoice_paid(data)

    return jsonify({"status": "Ignored because not fully paid."}), 200


def handle_invoice_paid(payload):
    """
    Called when Xendit confirms the user’s payment.
    Here you update wallet balance.
    """

    parsed_external_id = payload.get("external_id").split("_")
    amount = payload.get("amount")

    WalletServices.add_readits_to_wallet_from_paid_invoice_service(
        user_id=parsed_external_id[1],
        amount=amount,
    )

    return jsonify({"status": "Successful purchase."}), 200
