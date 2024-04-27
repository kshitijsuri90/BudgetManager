import uuid

from enum import Enum

class BudgetStatus(Enum):
    LOW = 1 # Less than 20% of the budget used
    NORMAL = 2 # Used more than 20% but less than 80% of the budget
    HIGH = 3   # Used more than 80% of the budget
    EXCEEDED = 4 # Exceeded the budget

    @classmethod
    def get_status(cls, value, allocated_amount):
        if value*100/allocated_amount < 20:
            return cls.LOW
        elif value*100/allocated_amount < 80:
            return cls.NORMAL
        elif value*100/allocated_amount <= 100:
            return cls.HIGH
        else:
            return cls.EXCEEDED

def get_budget_status_from_string(input_string):
    for enum_member in BudgetStatus:
        if input_string.upper() == enum_member.name:
            return enum_member
    return None

class Budget:
    def __init__(self, id, users, amount, currency, category, validity, status):
        self.id = id or str(uuid.uuid4())  # Generate a unique UUID for the budget
        self.users = users
        self.amount = amount
        self.currency = currency
        self.category = category
        self.validity = validity
        self.budget_status = status

    def to_dict(self):
        return {
            "id": self.id,
            "users": self.users,
            "amount": self.amount,
            "currency": self.currency,
            "category": self.category,
            "validity": self.validity,
            "budget_status": self.budget_status.name  # Assuming budget_status is an Enum
        }

    def __str__(self):
        return f"Budget ID: {self.id}\nUsers: {', '.join(self.users)}\nAmount: {self.amount} {self.currency}\nCategory: {self.category}\nValidity: {self.validity}"
