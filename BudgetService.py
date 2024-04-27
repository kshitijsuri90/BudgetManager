import sys
sys.path.append('/Users/kshitij.suri/Documents/NotBackedUp/Kniru')

from flask import Flask, request, jsonify
from budget.BudgetManager import BudgetManager
from transactions.TransactionManager import TransactionManager
from users.UserManager import UserManager

app = Flask(__name__)

# Budget methods
# GET method to retrieve all data
@app.route('/budget', methods=['GET'])
def get_all_budgets():
    try:
        budgets = budget_manager.get_all_budgets()
        return jsonify({'data': budgets, 'error': ''})
    except Exception as e:
        return jsonify({'data': '', 'error': str(e)}), 500

@app.route('/budget/<budget_id>', methods=['GET'])
def get_budget_by_id(budget_id):
    try:
        budget = budget_manager.get_budget(budget_id)
        if budget:
            return jsonify({'data': budget, 'error': ''})
        else:
            return jsonify({'data':'', 'error': 'Budget not found'}), 404
    except Exception as e:
        return jsonify({'data':'', 'error': str(e)}), 500

@app.route('/budget/user/<user_id>', methods=['GET'])
def get_user_budgets(user_id):
    budget = budget_manager.check_budget(user_id)
    if budget:
        return jsonify({'data':budget, 'error': ''})
    else:
        return jsonify({'data':'', 'error': 'Budget not found'}), 404

@app.route('/budget', methods=['POST'])
def add_budget():
    try:
        data = request.get_json()
        print('Data:', data)
        budget_manager.create_budget(data)
        return jsonify({"data": "Budget added successfully", 'error':''}), 201
    except Exception as e:
        return jsonify({'data':'', "error": str(e)}), 400

@app.route('/budget/<budget_id>', methods=['DELETE'])
def delete_budget_by_id(budget_id):
    try:
        budget_manager.delete_budget(budget_id)
        return jsonify({"data": f"Budget {budget_id} deleted successfully", 'error':''}), 200
    except Exception as e:
        return jsonify({'data':'', "error": str(e)}), 500

@app.route('/budget/<budget_id>', methods=['PUT'])
def update_budget_by_id(budget_id):
    try:
        data = request.get_json()
        print('Data:', data)
        # Retrieve the existing budget from the database
        budget = budget_manager.update_budget(data, budget_id)
        return jsonify({"data": f"Budget {budget_id} updated successfully", 'error':''}), 200
    except Exception as e:
        return jsonify({'data':'', "error": str(e)}), 400

# User endpoints
@app.route('/users', methods=['POST'])
def add_user():
    try:
        user_data = request.get_json()
        user_manager.add_user(user_data)
        return jsonify({"data": "User added successfully", 'error':''}), 201
    except Exception as e:
        return jsonify({'data':'', "error": str(e)}), 400

@app.route('/users', methods=['GET'])
def get_all_users():
    users = user_manager.get_all_users()
    return {"data" : users, 'error':''}

@app.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = user_manager.get_user(user_id)
        if user:
            return {"data" : user, 'error':''}
        else:
            return jsonify({'data':'', 'error': 'user not found'}), 404
    except Exception as e:
        return jsonify({'data':'', "error": str(e)}), 500

@app.route('/users', methods=['DELETE'])
def delete_all_users():
    try:
        user_manager.delete_all_users()
        return jsonify({"data": "All users deleted successfully", 'error':''}), 200
    except Exception as e:
        return jsonify({'data':'', "error": str(e)}), 500

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_manager.delete_user(user_id)
        return jsonify({"data": f"User {user_id} deleted successfully", 'error':''}), 200
    except Exception as e:
        return jsonify({'data':'', "error": str(e)}), 500

# Transactions endpoints
@app.route('/transactions', methods=['POST'])
def process_transactions():
    try:
        data = request.get_json()
        print('Data:', data)
        transaction_manager.process_transactions(data)
        return jsonify({"data": "Transactions processed successfully", 'error':''}), 201
    except Exception as e:
        return jsonify({'data':'', "error": str(e)}), 400

@app.route('/transactions/<user_id>', methods=['GET'])
def get_transactions_by_user(user_id):
    print('User ID:', user_id)
    data = transaction_manager.get_transactions_by_user(user_id)
    if data:
        return jsonify({'data': data, 'error':''})
    else:
        return jsonify({'data':'', 'error': 'user not found'}), 404

@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    transactions = transaction_manager.get_all_transactions()
    return jsonify({'data': transactions, 'error':''})

@app.route('/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        # Call the method in TransactionManager to delete the transaction
        transaction_manager.delete_transaction(transaction_id)
        return jsonify({"data": "Transaction deleted successfully", 'error':''}), 200
    except Exception as e:
        return jsonify({'data':'',"error": str(e)}), 400

@app.route('/transactions', methods=['DELETE'])
def delete_all_transactions():
    try:
        # Call the method in TransactionManager to delete all transactions
        transaction_manager.delete_all_transactions()
        return jsonify({"data": "All transactions deleted successfully", 'error':''}), 200
    except Exception as e:
        return jsonify({'data':'', "error": str(e)}), 400

if __name__ == '__main__':
    budget_manager = BudgetManager.get_instance()
    transaction_manager = TransactionManager.get_instance()
    user_manager = UserManager.get_instance()
    app.run(debug=True)