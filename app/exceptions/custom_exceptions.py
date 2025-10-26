class ValidationError(Exception):
    """Raised when user input validation fails."""

    pass


class EntityNotFoundError(Exception):
    """Raised when an entity is not found."""

    pass


class InvalidParameterError(ValidationError):
    """Raised when a query parameter has an invalid or disallowed value."""

    pass
