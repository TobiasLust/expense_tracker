# Expense Tracker

Expense Tracker is a command-line tool in Python that allows you to manage and track your expenses easily. You can add, delete, update, list, and export your expenses, as well as set a monthly budget and get a summary of your expenses.

## Features

- **Add Expenses**: Add new expenses with description, category, and amount.
- **Delete Expenses**: Remove an existing expense using its ID.
- **Update Expenses**: Update the description, category, or amount of an existing expense.
- **List Expenses**: Show all recorded expenses with an option to filter by category.
- **Expense Summary**: Display the total summary of expenses with the option to view only expenses for a specific month.
- **Set Budget**: Set a monthly budget to keep track of spending.
- **Export to CSV**: Export all expenses to a CSV file.

## Installation

1.Clone this repository to your local machine:

```bash
   git clone https://github.com/TobiasLust/expense_tracker.git
```

2.Navigate to the project directory:

```bash
    cd expense-tracker
```


## Project Structure 

main.py: Contains the main logic of the application.

expenses.json: File where expense data is stored. Like this:
![expenses.json](https://i.imgur.com/HzRhGtv.jpeg)

budgets.json: File where monthly budgets are stored.

When exporting to CSV:
![CSV](https://i.imgur.com/fTBEvK9.jpeg)

## Usage

You can use the tool directly from the command line. Here are some examples of how to use each command:

```bash
# Add an expense
python main.py add -d "Grocery shopping" -c "groceries" -a 200

# Delete an expense
python main.py delete --id 1

# Update an expense
python main.py update --id 1 -d "Weekly grocery shopping" -a 250

# List all expenses
python main.py list

# List expenses by category
python main.py list -c "groceries"

# Get a summary of expenses
python main.py summary

# Get a summary of expenses for a specific month
python main.py summary --month 5

# Set a monthly budget
python main.py setbudget --month 5 -a 1000

# Export expenses to a CSV file
python main.py export
```
