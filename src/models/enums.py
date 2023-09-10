from enum import Enum


class UserRoleEnum(Enum):
    admin = "admin"
    customer = "customer"


class ProductRatingEnum(Enum):
    very_bad = "1"
    bad = "2"
    average = "3"
    good = "4"
    very_good = "5"
