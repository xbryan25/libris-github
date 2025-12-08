export const usePasswordValidation = () => {
  const validatePassword = (
    password: string,
    username?: string,
    email?: string
  ): {
    valid: boolean;
    errors: string[];
    strength: "weak" | "medium" | "strong";
    percentage: number;
  } => {
    const errors: string[] = [];

    // Check minimum length
    if (password.length < 8) {
      errors.push("Password must be at least 8 characters long");
    }

    // Check for uppercase letter
    if (!/[A-Z]/.test(password)) {
      errors.push("Must contain at least one uppercase letter");
    }

    // Check for lowercase letter
    if (!/[a-z]/.test(password)) {
      errors.push("Must contain at least one lowercase letter");
    }

    // Check for digit
    if (!/\d/.test(password)) {
      errors.push("Must contain at least one number");
    }

    // Check for special character
    if (!/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/\\~`]/.test(password)) {
      errors.push("Must contain at least one special character");
    }

    // Check common passwords
    const commonPasswords = [
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
    ];
    if (commonPasswords.includes(password.toLowerCase())) {
      errors.push("Password is too common. Please choose a stronger password");
    }

    // Check if password contains username
    if (username && username.length >= 3) {
      if (password.toLowerCase().includes(username.toLowerCase())) {
        errors.push("Password cannot contain your username");
      }
    }

    // Check if password contains email prefix
    if (email) {
      const emailPrefix = email.split("@")[0];
      if (
        emailPrefix.length >= 3 &&
        password.toLowerCase().includes(emailPrefix.toLowerCase())
      ) {
        errors.push("Password cannot contain your email address");
      }
    }

    const strength = calculateStrength(password);
    const percentage = calculatePercentage(password);

    return {
      valid: errors.length === 0,
      errors,
      strength,
      percentage,
    };
  };

  const calculateStrength = (
    password: string
  ): "weak" | "medium" | "strong" => {
    let score = 0;

    // Length scoring
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (password.length >= 16) score++;

    // Character variety scoring
    if (/[A-Z]/.test(password)) score++;
    if (/[a-z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/\\~`]/.test(password)) score++;

    // Multiple of each type
    if ((password.match(/[A-Z]/g) || []).length >= 2) score++;
    if ((password.match(/\d/g) || []).length >= 2) score++;
    if (
      (password.match(/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/\\~`]/g) || []).length >=
      2
    )
      score++;

    if (score <= 3) return "weak";
    if (score <= 6) return "medium";
    return "strong";
  };

  const calculatePercentage = (password: string): number => {
    let score = 0;
    const maxScore = 10;

    // Length scoring (max 3 points)
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (password.length >= 16) score++;

    // Character variety (max 4 points)
    if (/[A-Z]/.test(password)) score++;
    if (/[a-z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/\\~`]/.test(password)) score++;

    // Bonus points (max 3 points)
    if ((password.match(/[A-Z]/g) || []).length >= 2) score++;
    if ((password.match(/\d/g) || []).length >= 2) score++;
    if (
      (password.match(/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/\\~`]/g) || []).length >=
      2
    )
      score++;

    return Math.round((score / maxScore) * 100);
  };

  const getStrengthColor = (strength: "weak" | "medium" | "strong"): string => {
    switch (strength) {
      case "weak":
        return "red";
      case "medium":
        return "yellow";
      case "strong":
        return "green";
      default:
        return "gray";
    }
  };

  const getStrengthText = (strength: "weak" | "medium" | "strong"): string => {
    switch (strength) {
      case "weak":
        return "Weak";
      case "medium":
        return "Medium";
      case "strong":
        return "Strong";
      default:
        return "";
    }
  };

  return {
    validatePassword,
    calculateStrength,
    calculatePercentage,
    getStrengthColor,
    getStrengthText,
  };
};