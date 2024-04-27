import sqlite3
import json
import uuid
from datetime import datetime

from transactions.Transaction import Transaction
from category.Category import is_category_member, CATEGORY
from users.UserManager import UserManager

class TransactionManager:
    _instance = None

    def __init__(self):
        self.db_file = 'transactions.db'
        self.create_table()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            TRANSACTION_ID VARCHAR,
                            USER VARCHAR,
                            CATEGORY VARCHAR,
                            AMOUNT INTEGER,
                            CURRENCY VARCHAR,
                            TIMESTAMP TIMESTAMP,
                            PRIMARY KEY (TRANSACTION_ID)
                        )''')
        conn.commit()
        conn.close()

    def add_transaction(self, transaction):
        print("Adding transaction to database")
        print(transaction)
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO transactions (TRANSACTION_ID, USER, CATEGORY, AMOUNT, CURRENCY, TIMESTAMP) VALUES (?, ?, ?, ?, ?, ?)''',
                           (transaction.id, transaction.user, transaction.category, transaction.amount, transaction.currency, transaction.timestamp))
            conn.commit()
            conn.close()
            print("Transaction added successfully")
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)
        except Exception as e:
            print("An error occurred add:", e)

    def get_all_transactions(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM transactions''')
        transactions = cursor.fetchall()
        db_transactions = [self.get_transaction_entity_from_db(transaction) for transaction in transactions]
        transaction_data = [transaction.to_dict() for transaction in db_transactions]
        json_data = json.dumps(transaction_data, ensure_ascii=False)
        conn.close()
        return json.loads(json_data)

    def get_transaction_entity_from_db(self, db_entry):
        transaction_id, user, category, amount, currency, timestamp = db_entry
        return Transaction(user, category, amount, currency, timestamp, transaction_id)

    def get_transactions_by_user(self, user):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM transactions WHERE USER = ?''', (user,))
        user_transactions = cursor.fetchall()
        db_transactions = [self.get_transaction_entity_from_db(transaction) for transaction in user_transactions]
        transaction_data = [transaction.to_dict() for transaction in db_transactions]
        json_data = json.dumps(transaction_data, ensure_ascii=False)
        conn.close()
        return json.loads(json_data)

    def get_transactions_by_user_with_time_category(self, user, timestamp, category):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        print('User:', user)
        cursor.execute('''SELECT * FROM transactions WHERE USER = ? AND TIMESTAMP >= ? AND CATEGORY = ?''', (user, timestamp, category))
        user_transactions = cursor.fetchall()
        conn.close()
        all_transactions = [self.get_transaction_entity_from_db(transaction) for transaction in user_transactions]
        return all_transactions

    def delete_transaction(self, transaction_id):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM transactions WHERE TRANSACTION_ID = ?''', (transaction_id,))
            conn.commit()
            conn.close()
            print("Transaction deleted successfully")
        except Exception as e:
            print("An error occurred:", e)

    def delete_all_transactions(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM transactions''')
            conn.commit()
            conn.close()
            print("All transactions deleted successfully")
        except Exception as e:
            print("An error occurred:", e)

    def process_transactions(self, data):
        try:
            user = data.get('user')
            _, all_present = UserManager.get_instance().check_user_existence([user])
            if not all_present:
                raise Exception("User list is invalid")
            transactions = data.get('transactions')
            print('Transactions:', transactions)
            for transaction_data in transactions:
                transaction_id = transaction_data.get('transaction_id')
                category = transaction_data.get('category')
                if(not is_category_member(category)):
                    print("Invalid category:", category)
                    raise Exception("Invalid category")

                amount = int(transaction_data.get('amount'))
                currency = transaction_data.get('currency')
                timestamp = transaction_data.get('timestamp')
                # Convert string to datetime object
                time_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                transaction = Transaction(user, category, amount, currency, timestamp)
                print(transaction)
                self.add_transaction(transaction)
                
            print("Transactions processed successfully")
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)
        except Exception as e:
            print("An error occurred:", e)