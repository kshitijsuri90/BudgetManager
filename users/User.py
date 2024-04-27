import uuid
import json

class User:
    def __init__(self, username, id=None):
        self.id = id or str(uuid.uuid4())
        self.username = username

    def __str__(self):
        return f"User ID: {self.user_id}\nUsername: {self.username}\n"
