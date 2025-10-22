from dataclasses import asdict, is_dataclass
from enum import Enum


def asdict_enum_safe(obj):
    if isinstance(obj, Enum):
        return obj.value
    elif is_dataclass(obj):
        return {k: asdict_enum_safe(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, (list, tuple)):
        return [asdict_enum_safe(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: asdict_enum_safe(v) for k, v in obj.items()}
    else:
        return obj
