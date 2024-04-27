import sqlite3
import json
import uuid
import json
from datetime import datetime

from budget.Budget import Budget, BudgetStatus, get_budget_status_from_string
from category.Category import is_category_member, CATEGORY
from transactions.TransactionManager import TransactionManager, Transaction

class BudgetManager:
    """
    A class that manages budgets by interacting with a SQLite database.
    """

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
        """
        Creates the 'budgets' table in the SQLite database if it doesn't exist.
        """
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
        """
        Creates a new budget in the database.

        Args:
            data (dict): A dictionary containing the budget details.

        Raises:
            Exception: If the category is invalid or if there is an error while parsing the JSON.

        Returns:
            None
        """
        try:
            users = data.get('users')
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
        """
        Retrieves all budgets from the database.

        Returns:
            list: A list of dictionaries representing the budgets.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM budgets''')
        budgets = cursor.fetchall()
        db_budget = [self.get_budget_object_from_db(budget) for budget in budgets]
        budget_data = [budget.to_dict() for budget in db_budget]
        json_data = json.dumps(budget_data, ensure_ascii=False)
        conn.close()
        return json.loads(json_data)

    # Rest of the code...
