import sys
sys.path.append('/Users/kshitij.suri/Documents/NotBackedUp/Kniru')

from flask import Flask, request, jsonify
from budget.BudgetManager import BudgetManager
from transactions.TransactionManager import TransactionManager
from users.UserManager import UserManager

app = Flask(__name__)

# Budget methods

def get_all_budgets():
    """
    Retrieve all budgets.
    """
    budgets = budget_manager.get_all_budgets()
    return jsonify(budgets)

def get_budget_by_id(budget_id):
    """
    Retrieve a budget by its ID.
    """
    budget = budget_manager.get_budget(budget_id)
    if budget:
        return jsonify({'output': budget})
    else:
        return jsonify({'error': 'Budget not found'}), 404

def get_user_budgets(user_id):
    """
    Retrieve budgets associated with a user.
    """
    budget = budget_manager.check_budget(user_id)
    if budget:
        return jsonify({'output': budget})
    else:
        return jsonify({'error': 'Budget not found'}), 404

def add_budget():
    """
    Add a new budget.
    """
    try:
        data = request.get_json()
        print('Data:', data)
        budget_manager.create_budget(data)
        return jsonify({"message": "Transactions processed successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_budget_by_id(budget_id):
    """
    Delete a budget by its ID.
    """
    try:
        budget_manager.delete_budget(budget_id)
        return jsonify({"message": f"Budget {budget_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_budget_by_id(budget_id):
    """
    Update a budget by its ID.
    """
    try:
        data = request.get_json()
        print('Data:', data)
        # Retrieve the existing budget from the database
        budget = budget_manager.update_budget(data, budget_id)
        return jsonify({"message": f"Budget {budget_id} updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# User endpoints

def add_user():
    """
    Add a new user.
    """
    try:
        user_data = request.get_json()
        user_manager.add_user(user_data)
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_all_users():
    """
    Retrieve all users.
    """
    users = user_manager.get_all_users()
    return {"data" : users}

def get_user_by_id(user_id):
    """
    Retrieve a user by their ID.
    """
    user = user_manager.get_user(user_id)
    if user:
        return {"data" : user}
    else:
        return jsonify({'error': 'user not found'}), 404

def delete_all_users():
    """
    Delete all users.
    """
    try:
        user_manager.delete_all_users()
        return jsonify({"message": "All users deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_user(user_id):
    """
    Delete a user by their ID.
    """
    try:
        user_manager.delete_user(user_id)
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Transactions endpoints

def process_transactions():
    """
    Process transactions.
    """
    try:
        data = request.get_json()
        print('Data:', data)
        transaction_manager.process_transactions(data)
        return jsonify({"message": "Transactions processed successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_transactions_by_user(user_id):
    """
    Retrieve transactions by user ID.
    """
    print('User ID:', user_id)
    data = transaction_manager.get_transactions_by_user(user_id)
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'user not found'}), 404

def get_all_transactions():
    """
    Retrieve all transactions.
    """
    transactions = transaction_manager.get_all_transactions()
    return jsonify(transactions)

def delete_transaction(transaction_id):
    """
    Delete a transaction by its ID.
    """
    try:
        # Call the method in TransactionManager to delete the transaction
        transaction_manager.delete_transaction(transaction_id)
        return jsonify({"message": "Transaction deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_all_transactions():
    """
    Delete all transactions.
    """
    try:
        # Call the method in TransactionManager to delete all transactions
        transaction_manager.delete_all_transactions()
        return jsonify({"message": "All transactions deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    budget_manager = BudgetManager.get_instance()
    transaction_manager = TransactionManager.get_instance()
    user_manager = UserManager.get_instance()
    app.run(debug=True)