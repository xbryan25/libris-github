from flask import current_app

from .repository import WalletRepository

import xendit

from xendit.apis import InvoiceApi

from xendit.invoice.model.create_invoice_request import CreateInvoiceRequest

from datetime import datetime


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

    @staticmethod
    def buy_readits_service(user_id, amount_needed_in_pack, readits_from_pack) -> str:
        xendit.set_api_key(current_app.config.get("XENDIT_SECRET_KEY", ""))

        api_client = xendit.ApiClient()
        api_instance = InvoiceApi(api_client)

        external_id = f"readits_{user_id}_{int(datetime.now().timestamp())}"
        payer_email = "bryanaganp25@gmail.com"
        description = f"Purchase {int(readits_from_pack)} readits"

        create_invoice_request = CreateInvoiceRequest(
            external_id=external_id,
            amount=amount_needed_in_pack,
            payer_email=payer_email,
            description=description,
            invoice_duration=1800.0,  # Invoice expires after 30 minutes
        )

        invoice = api_instance.create_invoice(create_invoice_request)  # type: ignore[arg-type]

        return invoice["invoice_url"]

    @staticmethod
    def add_readits_to_wallet_from_paid_invoice_service(user_id, amount, last_updated):

        amount_to_readits_dict = {100: 200, 150: 600, 350: 1000, 750: 5000}

        if amount not in amount_to_readits_dict:
            readits_to_add = 0
        else:
            readits_to_add = amount_to_readits_dict[amount]

        WalletRepository.add_readits_to_wallet_from_paid_invoice(
            user_id, readits_to_add, last_updated
        )

    @staticmethod
    def add_transaction_service(user_id, amount, transaction_date):

        amount_to_readits_dict = {100: 200, 150: 600, 350: 1000, 750: 5000}

        if amount not in amount_to_readits_dict:
            readits_transaction_amount = 0
        else:
            readits_transaction_amount = amount_to_readits_dict[amount]

        WalletRepository.add_transaction(
            readits_transaction_amount, transaction_date, "topup", user_id
        )
