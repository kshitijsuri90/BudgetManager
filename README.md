# Budget Management API

## Overview

The Budget Management API is a Flask-based web service for managing budgets, users, and transactions. It provides various endpoints for performing CRUD (Create, Read, Update, Delete) operations on budgets, users, and transactions.

## Dependencies

    Flask
    SQLite

## Installation

1. Clone the repository:

```bash
git clone https://github.com/kshitijsuri90/BudgetManager.git
```


2. Run the flask script:
```bash
python3 BudgetService.py
```

## Usage

Endpoints

    Budgets
        GET /budget: Retrieve all budgets.
        GET /budget/{budget_id}: Retrieve a budget by its ID.
        POST /budget: Add a new budget.
        PUT /budget/{budget_id}: Update a budget by its ID.
        DELETE /budget/{budget_id}: Delete a budget by its ID.

    Users
        POST /users: Add a new user.
        GET /users: Retrieve all users.
        GET /users/{user_id}: Retrieve a user by their ID.
        DELETE /users/{user_id}: Delete a user by their ID.
        DELETE /users: Delete all users.

    Transactions
        POST /transactions: Process transactions.
        GET /transactions/{user_id}: Retrieve transactions by user ID.
        GET /transactions: Retrieve all transactions.
        DELETE /transactions/{transaction_id}: Delete a transaction by its ID.
        DELETE /transactions: Delete all transactions.

## Modules

Three modules, each having its own DB and manager following singleton design instance:

1. Users
2. Transactions
3. Budget
