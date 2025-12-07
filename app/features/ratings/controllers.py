from flask import request, jsonify, Response
from flask_jwt_extended import get_jwt_identity
import traceback

from .services import RatingServices


class RatingControllers:

    @staticmethod
    def submit_rental_rating(rental_id: str) -> tuple[Response, int]:
        """
        POST /api/rentals/<rental_id>/rate

        Request body:
        {
            "rating": 5,
            "review": "Great!",
            "from": "rental"
        }
        """
        try:
            rater_id = get_jwt_identity()

            if not rater_id:
                return jsonify({"error": "Not authenticated"}), 401

            data = request.get_json()

            if not data:
                return jsonify({"error": "No data provided"}), 400

            score = data.get("rating")
            comment = data.get("review", "")
            from_perspective = data.get("from")

            # Validate
            if not score or not isinstance(score, int) or score < 1 or score > 5:
                return jsonify({"error": "Rating must be 1-5"}), 400

            if from_perspective not in ["rental", "lending"]:
                return jsonify({"error": "Invalid 'from' parameter"}), 400

            # Submit
            result = RatingServices.submit_rental_rating(
                rental_id, rater_id, score, comment, from_perspective
            )

            if not result["success"]:
                return jsonify({"error": result["error"]}), 400

            return jsonify({"message": result["message"]}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def submit_purchase_rating(purchase_id: str) -> tuple[Response, int]:
        """
        POST /api/ratings/purchase/<purchase_id>/rate

        Request body:
        {
            "rating": 5,
            "review": "Great!",
            "from": "purchase" or "sale"
        }
        """
        try:
            rater_id = get_jwt_identity()

            if not rater_id:
                return jsonify({"error": "Not authenticated"}), 401

            data = request.get_json()

            if not data:
                return jsonify({"error": "No data provided"}), 400

            score = data.get("rating")
            comment = data.get("review", "")
            from_perspective = data.get("from")

            # Validate
            if not score or not isinstance(score, int) or score < 1 or score > 5:
                return jsonify({"error": "Rating must be 1-5"}), 400

            if from_perspective not in ["purchase", "sale"]:
                return jsonify({"error": "Invalid 'from' parameter"}), 400

            # Submit
            result = RatingServices.submit_purchase_rating(
                purchase_id, rater_id, score, comment, from_perspective
            )

            if not result["success"]:
                return jsonify({"error": result["error"]}), 400

            return jsonify({"message": result["message"]}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_ratings_from_purchase_for_user_controller(
        purchase_id: str,
    ) -> tuple[Response, int]:

        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"error": "Not authenticated"}), 401

            ratings_with_comments = (
                RatingServices.get_ratings_from_purchase_for_user_service(
                    user_id, purchase_id
                )
            )

            return jsonify(ratings_with_comments), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
