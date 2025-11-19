import enum


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    others = "others"
    prefer_not_to_say = "prefer_not_to_say"


class BookConditionEnum(enum.Enum):
    new = "new"
    good = "good"
    used = "used"
    worn = "worn"


class BookAvailabilityEnum(enum.Enum):
    rent = "rent"
    purchase = "purchase"
    both = "both"


class NotificationTypeEnum(enum.Enum):
    rent = "rent"
    purchase = "purchase"
    system = "system"
