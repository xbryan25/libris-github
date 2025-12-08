import re
from typing import Dict, Optional, Any


class PasswordValidator:
    """Utility class for password strength validation"""

    # Common weak passwords to reject
    COMMON_PASSWORDS = [
        "password",
        "123456",
        "password123",
        "12345678",
        "qwerty",
        "abc123",
        "monkey",
        "letmein",
        "password1",
        "admin123",
    ]

    @staticmethod
    def validate_password(
        password: str, username: Optional[str] = None, email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate password strength according to requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        - Not a common password
        - Not containing username or email

        Returns:
            Dict with 'valid' (bool), 'errors' (list[str]), 'strength' (str)
        """
        errors = []

        # Check minimum length
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")

        # Check for uppercase letter
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")

        # Check for lowercase letter
        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")

        # Check for digit
        if not re.search(r"\d", password):
            errors.append("Password must contain at least one number")

        # Check for special character
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{}\|;:,.<>?/\\~`]", password):
            errors.append("Password must contain at least one special character")

        # Check against common passwords
        if password.lower() in PasswordValidator.COMMON_PASSWORDS:
            errors.append("Password is too common. Please choose a stronger password")

        # Check if password contains username
        if username and len(username) >= 3:
            if username.lower() in password.lower():
                errors.append("Password cannot contain your username")

        # Check if password contains email prefix
        if email:
            email_prefix = email.split("@")[0]
            if len(email_prefix) >= 3 and email_prefix.lower() in password.lower():
                errors.append("Password cannot contain your email address")

        # Calculate strength
        strength = PasswordValidator.calculate_strength(password)

        return {"valid": len(errors) == 0, "errors": errors, "strength": strength}

    @staticmethod
    def calculate_strength(password: str) -> str:
        """
        Calculate password strength based on various criteria
        Returns: 'weak', 'medium', or 'strong'
        """
        score = 0

        # Length scoring
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1

        # Character variety scoring
        if re.search(r"[A-Z]", password):
            score += 1
        if re.search(r"[a-z]", password):
            score += 1
        if re.search(r"\d", password):
            score += 1
        if re.search(r"[!@#$%^&*()_+\-=\[\]{}\|;:,.<>?/\\~`]", password):
            score += 1

        # Multiple of each type adds more strength
        if len(re.findall(r"[A-Z]", password)) >= 2:
            score += 1
        if len(re.findall(r"\d", password)) >= 2:
            score += 1
        if len(re.findall(r"[!@#$%^&*()_+\-=\[\]{}\|;:,.<>?/\\~`]", password)) >= 2:
            score += 1

        # Determine strength level
        if score <= 3:
            return "weak"
        elif score <= 6:
            return "medium"
        else:
            return "strong"

    @staticmethod
    def get_strength_percentage(password: str) -> int:
        """
        Get password strength as percentage (0-100)
        Used for progress bar visualization
        """
        score = 0
        max_score = 10

        # Length scoring (max 3 points)
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1

        # Character variety (max 4 points)
        if re.search(r"[A-Z]", password):
            score += 1
        if re.search(r"[a-z]", password):
            score += 1
        if re.search(r"\d", password):
            score += 1
        if re.search(r"[!@#$%^&*()_+\-=\[\]{}\|;:,.<>?/\\~`]", password):
            score += 1

        # Bonus points (max 3 points)
        if len(re.findall(r"[A-Z]", password)) >= 2:
            score += 1
        if len(re.findall(r"\d", password)) >= 2:
            score += 1
        if len(re.findall(r"[!@#$%^&*()_+\-=\[\]{}\|;:,.<>?/\\~`]", password)) >= 2:
            score += 1

        return int((score / max_score) * 100)
