class ValidationError(Exception):
    """Raised when user input validation fails."""

    pass


class EntityNotFoundError(Exception):
    """Raised when an entity is not found."""

    pass


class InvalidParameterError(ValidationError):
    """Raised when a query parameter has an invalid or disallowed value."""

    pass


class EmailInUseByGoogleError(Exception):
    """Raised when an email is already registered via Google Sign-In."""

    pass
