from .repository import RatingRepository


class RatingServices:

    @staticmethod
    def submit_rating(
        rental_id: str, rater_id: str, score: int, comment: str, from_perspective: str
    ) -> dict:
        """
        Submit a rating.

        Steps:
        1. Get rental info
        2. Verify rental is completed
        3. Determine who is rating whom
        4. Insert rating
        5. Update flag (user_rated or owner_rated)
        """

        # Get rental info
        rental = RatingRepository.get_rental_info(rental_id)

        if not rental:
            return {"success": False, "error": "Rental not found"}

        # Check if completed
        if rental["rent_status"] != "completed":
            return {"success": False, "error": "Rental must be completed to rate"}

        renter_id = str(rental["user_id"])
        owner_id = str(rental["owner_id"])

        # Determine who rates whom
        if from_perspective == "rental":
            # Renter rating owner
            if rater_id != renter_id:
                return {"success": False, "error": "Not authorized"}

            if rental["user_rated"]:
                return {"success": False, "error": "Already rated"}

            rated_user_id = owner_id
            flag = "user_rated"

        elif from_perspective == "lending":
            # Owner rating renter
            if rater_id != owner_id:
                return {"success": False, "error": "Not authorized"}

            if rental["owner_rated"]:
                return {"success": False, "error": "Already rated"}

            rated_user_id = renter_id
            flag = "owner_rated"
        else:
            return {"success": False, "error": "Invalid perspective"}

        # Insert rating
        result = RatingRepository.insert_rating(
            rater_id,
            rated_user_id,
            score,
            comment,
            rental_id=rental_id,
            purchase_id=None,
        )

        if not result:
            return {"success": False, "error": "Failed to insert rating"}

        # Update flag
        if flag == "user_rated":
            RatingRepository.update_user_rated_flag(rental_id)
        else:
            RatingRepository.update_owner_rated_flag(rental_id)

        return {"success": True, "message": "Rating submitted"}

    @staticmethod
    def submit_purchase_rating(
        purchase_id: str, rater_id: str, score: int, comment: str, from_perspective: str
    ) -> dict:
        """
        Submit a rating for a purchase.
        """
        try:
            # Get purchase info
            purchase = RatingRepository.get_purchase_info(purchase_id)

            if not purchase:
                return {"success": False, "error": "Purchase not found"}

            buyer_id = str(purchase["user_id"])
            seller_id = str(purchase["owner_id"])  # Uses original_owner_id from query

            # Check if already rated
            existing_rating = RatingRepository.check_existing_purchase_rating(
                purchase_id, rater_id
            )

            if existing_rating:
                return {"success": False, "error": "Already rated this transaction"}

            # Determine who rates whom
            if from_perspective == "purchase":
                # Buyer rating seller
                if rater_id != buyer_id:
                    return {"success": False, "error": "Not authorized"}

                if purchase["user_rated"]:
                    return {"success": False, "error": "Already rated"}

                rated_user_id = seller_id
                flag = "user_rated"

            elif from_perspective == "sale":
                # Seller rating buyer
                if rater_id != seller_id:  # Now correctly compares with original seller
                    return {"success": False, "error": "Not authorized"}

                if purchase["owner_rated"]:
                    return {"success": False, "error": "Already rated"}

                rated_user_id = buyer_id
                flag = "owner_rated"
            else:
                return {"success": False, "error": "Invalid perspective"}

            # Insert rating
            result = RatingRepository.insert_rating(
                rater_id,
                rated_user_id,
                score,
                comment,
                rental_id=None,
                purchase_id=purchase_id,
            )

            if not result:
                return {"success": False, "error": "Failed to insert rating"}

            # Update flag
            if flag == "user_rated":
                RatingRepository.update_purchase_user_rated_flag(purchase_id)
            else:
                RatingRepository.update_purchase_owner_rated_flag(purchase_id)

            return {"success": True, "message": "Rating submitted"}

        except Exception as e:
            import traceback

            traceback.print_exc()
            return {"success": False, "error": str(e)}
