import sqlite3
import json
from users.User import User

class UserManager:
    _instance = None

    def __init__(self):
        self.db_file = 'users.db'
        self.create_table()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def create_table(self):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        print('Adding table')
        cursor.execute('''CREATE TABLE IF NOT EXISTS USERS (
                            UUID VARCHAR, NAME VARCHAR, 
                            PRIMARY KEY (UUID))''')
        conn.commit()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", ("USERS",))
        user = User("Test")
        uuid = user.id
        cursor.execute('''INSERT INTO USERS (UUID, NAME) VALUES (?, ?)''', (uuid, "Test"))
        result = cursor.fetchone()
        conn.close()

    def add_user(self, data):
        print("Adding user")
        print("Data: ", data)
        username = data.get('username')
        print(username)
        if username:
            user = User(username)
            uuid = user.id
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO USERS (UUID, NAME) VALUES (?, ?)''', (uuid, username))
            conn.commit()
            conn.close()
            print("User %s added successfully" % uuid)
        else:
            print("Error: Username not provided")

    def get_user(self, uuid):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM USERS WHERE UUID = ?''', (uuid,))
        user = cursor.fetchone()
        user_obj = self.get_user_object_from_db(user)
        json_data = json.dumps(user_obj.__dict__)
        conn.close()
        return json.loads(json_data)

    def get_user_object_from_db(self, db_entry):
        uuid, name = db_entry
        return User(name, uuid)

    def get_all_users(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM USERS''')
        users = cursor.fetchall()
        db_users = [self.get_user_object_from_db(user) for user in users]
        users_data = [user.__dict__ for user in db_users]
        json_data = json.dumps(users_data, ensure_ascii=False)
        conn.close()
        return json.loads(json_data)

    def delete_user(self, uuid):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM USERS WHERE UUID = ?''', (uuid,))
            conn.commit()
            conn.close()
            print(f"User {uuid} deleted successfully")
        except Exception as e:
            print("An error occurred:", e)

    def delete_all_users(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM USERS''')
            conn.commit()
            conn.close()
            print("All users deleted successfully")
        except Exception as e:
            print("An error occurred:", e)