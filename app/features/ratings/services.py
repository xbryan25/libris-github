from .repository import RatingRepository

from typing import Any


class RatingServices:

    @staticmethod
    def submit_rental_rating(
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

        try:
            rater_trust_score = RatingRepository.get_user_trust_score(rater_id)

            target_current_score = RatingRepository.get_user_trust_score(rated_user_id)

            impact = RatingServices._calculate_weighted_impact(score, rater_trust_score)

            new_score = max(0, min(1000, target_current_score + impact))

            RatingRepository.update_user_trust_score(rated_user_id, new_score)

        except Exception as e:
            print(f"Error updating trust score: {e}")

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
            # ... [Validation logic matches your code] ...

            # Get purchase info
            purchase = RatingRepository.get_purchase_info(purchase_id)
            if not purchase:
                return {"success": False, "error": "Purchase not found"}

            buyer_id = str(purchase["user_id"])
            seller_id = str(purchase["owner_id"])

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
                if rater_id != seller_id:
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

            try:
                rater_trust_score = RatingRepository.get_user_trust_score(rater_id)
                target_current_score = RatingRepository.get_user_trust_score(
                    rated_user_id
                )

                impact = RatingServices._calculate_weighted_impact(
                    score, rater_trust_score
                )

                # 3. Apply and Clamp
                new_score = max(0, min(1000, target_current_score + impact))

                RatingRepository.update_user_trust_score(rated_user_id, new_score)

            except Exception as e:
                print(f"Error updating trust score for purchase: {e}")

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

    @staticmethod
    def _calculate_weighted_impact(rating: int, rater_score: int) -> int:
        """
        Calculate score impact scaled by the rater's credibility.
        Formula: Base Impact * (0.5 + (RaterScore / 2000))
        """
        base = 0
        if rating == 5:
            base = 15
        elif rating == 4:
            base = 10
        elif rating == 3:
            base = 0
        elif rating == 2:
            base = -10
        elif rating == 1:
            base = -30

        multiplier = 0.5 + (rater_score / 2000)

        return int(base * multiplier)

    @staticmethod
    def get_ratings_from_purchase_for_user_service(
        purchase_id: str, user_id
    ) -> dict[str, Any] | None:

        ratings_with_comments = None

        rater_ratings_with_comments = (
            RatingRepository.get_ratings_from_purchase_from_rater(user_id, purchase_id)
        )

        rated_user_ratings_with_comments = (
            RatingRepository.get_ratings_from_purchase_from_rated_user(
                user_id, purchase_id
            )
        )

        if rater_ratings_with_comments and rated_user_ratings_with_comments:
            ratings_with_comments = (
                rater_ratings_with_comments | rated_user_ratings_with_comments
            )

        return ratings_with_comments
