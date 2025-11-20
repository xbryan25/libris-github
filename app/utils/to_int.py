def to_int(value: str | int | None, default: int = 0) -> int:
    """Safely convert str to int"""

    try:
        return int(value) if value is not None else default
    except ValueError:
        return default
