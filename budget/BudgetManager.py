import sqlite3
import json
import uuid
import json
from datetime import datetime

from budget.Budget import Budget, BudgetStatus, get_budget_status_from_string
from category.Category import is_category_member, CATEGORY
from transactions.TransactionManager import TransactionManager, Transaction
from users.UserManager import UserManager

class BudgetManager:
    _instance = None

    def __init__(self):
        self.db_file = 'budget.db'
        self.create_table()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                            id VARCHAR,
                            users TEXT,
                            amount REAL,
                            currency VARCHAR,
                            category VARCHAR,
                            validity TIMESTAMP,
                            status VARCHAR,
                            PRIMARY KEY (id)
                        )''')
        conn.commit()
        conn.close()

    def create_budget(self, data):
        try:
            users = data.get('users')
            _, all_present = UserManager.get_instance().check_user_existence(users)
            if not all_present:
                raise Exception("User list is invalid")
            amount = data.get('amount')
            currency = data.get('currency')
            category = data.get('category')
            category = data.get('category')
            if(not is_category_member(category)):
                print("Invalid category:", category)
                raise Exception("Invalid category")
            validity = data.get('validity')
            # Convert string to datetime object
            time_obj = datetime.strptime(validity, '%Y-%m-%d %H:%M:%S')
            
            budget = Budget(None, users, amount, currency, category, validity, BudgetStatus.LOW)
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO budgets (id, users, amount, currency, category, validity, status) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (str(budget.id), json.dumps(budget.users), budget.amount, budget.currency, budget.category, budget.validity, budget.budget_status.name))
            conn.commit()
            conn.close()
            print("Budget %s added successfully" % budget)
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)
            raise e
        except Exception as e:
            print("An error occurred:", e)
            raise e

    def get_all_budgets(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM budgets''')
        budgets = cursor.fetchall()
        db_budget = [self.get_budget_object_from_db(budget) for budget in budgets]
        budget_data = [budget.to_dict() for budget in db_budget]
        json_data = json.dumps(budget_data, ensure_ascii=False)
        conn.close()
        return json.loads(json_data)

    def get_budget(self, budget_id):
        self.refresh_budget_status(budget_id)
        return self.get_budget_entity_by_id(budget_id)

    def get_budget_object_from_db(self, db_entry):
        id, users_json, amount, currency, category, validity, status = db_entry
        users = json.loads(users_json)
        return Budget(id, users, amount, currency, category, validity, get_budget_status_from_string(status))
        
    def get_budget_entity_by_id(self, budget_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM budgets WHERE id = ?''', (budget_id,))
        budget = cursor.fetchone()
        if budget:
            budget_object = self.get_budget_object_from_db(budget)
            data = budget_object.to_dict()
            json_data = json.dumps(data, ensure_ascii=False)
            conn.close()
            return json.loads(json_data)
        else:
            conn.close()
            return None

    def refresh_budget_status(self, budget_id):
        # Step 1: Retrieve users associated with the budget
        budget = self.get_budget_entity_by_id(budget_id)
        print('Budget:', budget)
        if budget:
            users = budget.get("users")  # Assuming users are stored as JSON in the database
            total_amount = 0
            
            # Step 2: Use TransactionManager instance to get transactions for each user
            transaction_manager = TransactionManager.get_instance()
            for user in users:
                user_transactions = transaction_manager.get_transactions_by_user_with_time_category(user, budget.get("validity"), budget.get("category"))
                print('User transactions:', user_transactions)
                for transaction in user_transactions:
                    total_amount +=  transaction.amount # Assuming amount is at index 3 in the transaction tuple
            
            status = BudgetStatus.get_status(total_amount, budget.get("amount"))
            # Step 4: Update the budget status in the database
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''UPDATE budgets SET status = ? WHERE id = ?''', (status.name, budget_id))
            conn.commit()
            conn.close()
        else:
            print("Budget not found")
            return None

    def delete_budget(self, budget_id):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM budgets WHERE id = ?''', (budget_id,))
            conn.commit()
            conn.close()
            print("Budget deleted successfully")
        except Exception as e:
            print("An error occurred:", e)
            raise e

    def update_budget(self, budget_json, id):
        budget = Budget(id, budget_json['users'], budget_json['amount'], budget_json['currency'], budget_json['category'], budget_json['validity'], BudgetStatus.LOW) 
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''UPDATE budgets SET users = ?, amount = ?, currency = ?, category = ?, validity = ? WHERE id = ?''',
                           (json.dumps(budget.users), budget.amount, budget.currency, budget.category, budget.validity, budget.id))
            conn.commit()
            conn.close()
            print("Budget updated successfully")
        except Exception as e:
            print("An error occurred:", e)
            raise e