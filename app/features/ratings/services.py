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
        result = RatingRepository.insert_rating(rater_id, rated_user_id, score, comment)

        if not result:
            return {"success": False, "error": "Failed to insert rating"}

        try:
            current_score = RatingRepository.get_user_trust_score(rated_user_id)

            impact = RatingServices._calculate_score_impact(score)

            new_score = max(0, min(1000, current_score + impact))

            RatingRepository.update_user_trust_score(rated_user_id, new_score)

        except Exception as e:
            print(f"Error updating trust score: {e}")

        if flag == "user_rated":
            RatingRepository.update_user_rated_flag(rental_id)
        else:
            RatingRepository.update_owner_rated_flag(rental_id)

        return {"success": True, "message": "Rating submitted"}

    @staticmethod
    def _calculate_score_impact(rating: int) -> int:
        if rating == 5:
            return 15
        if rating == 4:
            return 10
        if rating == 3:
            return 0
        if rating == 2:
            return -10
        if rating == 1:
            return -30
        return 0
