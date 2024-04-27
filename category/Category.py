from enum import Enum

class CATEGORY(Enum):
    TRAVEL = 1
    FOOD = 2
    SHOPPING = 3

def is_category_member(value):
    try:
        getattr(CATEGORY, value)
        return True
    except AttributeError:
        return False