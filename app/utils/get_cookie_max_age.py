import os


# Result will be in minutes
def get_cookie_max_age(default: str = "5") -> int:
    value = os.getenv("COOKIE_MAX_AGE", default)

    try:
        return int(value) * 60
    except ValueError:
        print(
            f"WARNING: COOKIE_MAX_AGE='{value}' is not a valid integer. Using default={default}"
        )
        return int(default) * 60


# Result will be in days
def get_refresh_cookie_max_age(default: str = "5") -> int:
    value = os.getenv("REFRESH_COOKIE_MAX_AGE", default)

    try:
        return int(value) * 60 * 60 * 24
    except ValueError:
        print(
            f"WARNING: REFRESH_COOKIE_MAX_AGE='{value}' is not a valid integer. Using default={default}"
        )
        return int(default) * 60 * 60 * 24
