import uuid

class Transaction:
    def __init__(self, user, category, amount, currency, timestamp, id=None):
        self.id = id or str(uuid.uuid4())  # Generate a unique UUID for the transaction
        self.user = user
        self.category = category
        self.amount = amount
        self.currency = currency
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "category": self.category,
            "amount": self.amount,
            "currency": self.currency,
            "timestamp": self.timestamp
        }

    def __str__(self):
        return f"Transaction ID: {self.id}\nUser: {self.user}\nCategory: {self.category}\nAmount: {self.amount} {self.currency}\nTimestamp: {self.timestamp}"
