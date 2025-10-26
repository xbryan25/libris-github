from typing import Any
import re


def to_camel_case(s: str) -> str:
    parts = re.split(r"[_\s]+", s)
    return parts[0].lower() + "".join(word.capitalize() for word in parts[1:])


def dict_keys_to_camel(d: dict[str, Any]) -> dict[str, Any]:
    return {to_camel_case(k): v for k, v in d.items()}
