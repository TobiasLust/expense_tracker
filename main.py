import json
import argparse
import calendar
import csv
from datetime import date

EXPENSES_FILE = "expenses.json"
BUDGETS_FILE = "budgets.json"


def main():
    parser = argparse.ArgumentParser("Expense Tracker")
    subparser = parser.add_subparsers(dest="command")

    # "ADD" COMMAND
    parser_add = subparser.add_parser("add", help="Add a new expense")
    parser_add.add_argument(
        "-d",
        "--description",
        type=str,
        required=True,
        help="Description of the expense",
    )
    parser_add.add_argument(
        "-c",
        "--category",
        type=str,
        required=False,
        choices=[
            "housing",
            "groceries",
            "transportation",
            "healthcare",
            "entertainment",
            "savings",
            "clothing",
            "others",
        ],
        default="Others",
        help="Category of expense",
    )
    parser_add.add_argument(
        "-a", "--amount", type=int, required=True, help="Amount of the expense"
    )

    # "DELETE" COMMAND
    parser_delete = subparser.add_parser("delete", help="Delete expense by id")
    parser_delete.add_argument(
        "--id", type=int, required=True, help="Id from expense Example: --id 1"
    )

    # "UPDATE" COMMAND
    parser_update = subparser.add_parser("update", help="Update expense by id")
    parser_update.add_argument(
        "--id", type=int, required=True, help="Id from expense Example: --id 1"
    )
    parser_update.add_argument(
        "-d",
        "--description",
        type=str,
        required=False,
        help="Description of the expense",
    )
    parser_update.add_argument(
        "-a", "--amount", type=int, required=False, help="Amount of the expense"
    )
    parser_update.add_argument(
        "-c",
        "--category",
        type=str,
        required=False,
        choices=[
            "housing",
            "groceries",
            "transportation",
            "healthcare",
            "entertainment",
            "savings",
            "clothing",
            "others",
        ],
        default="Others",
        help="Category of expense",
    )

    # "LIST" COMMAND
    parser_list = subparser.add_parser("list", help="View all expenses")
    parser_list.add_argument(
        "-c",
        "--category",
        type=str,
        required=False,
        choices=[
            "housing",
            "groceries",
            "transportation",
            "healthcare",
            "entertainment",
            "savings",
            "clothing",
            "others",
        ],
        help="Amount of the expense",
    )

    # "SUMMARY" COMMAND
    parser_summary = subparser.add_parser(
        "summary", help="Summary all the expenses amount"
    )
    parser_summary.add_argument(
        "--month", type=int, required=False, help="Summary only month expenses"
    )

    # "SET BUDGET" COMMAND
    parser_setbudget = subparser.add_parser(
        "setbudget", help="Set budget for month expenses"
    )
    parser_setbudget.add_argument(
        "--month",
        type=int,
        choices=range(1, 13),
        required=True,
        help="Month for set budget",
    )
    parser_setbudget.add_argument(
        "-a", "--amount", type=int, required=True, help="Amount for set budget"
    )

    # "EXPORT" COMMAND
    parser_export = subparser.add_parser("export", help="Export expenses to csv")

    # Check command in cli
    args = parser.parse_args()

    if args.command == "add":

        if check_amount(args.amount):
            add_expense(create_expense(args.description, args.amount, args.category))
            print("Expense added")
    elif args.command == "delete":
        if delete_expense(args.id):
            print(f"Delete expense id:{args.id}")
        else:
            print(f"Expense id:{args.id} not exist")

    elif args.command == "update":
        if update_expense(args.id, args.description, args.amount, args.category):
            print(f"Expense id:{args.id} updated")
        else:
            print(f"Expense not updated")
    elif args.command == "list":
        if args.category:
            view_expenses_cat(args.category)
        else:
            view_expenses()
    elif args.command == "summary":
        if args.month == 0 or args.month:
            if check_month(args.month):
                month_name = calendar.month_name[args.month]
                if sum_month_expenses(args.month):

                    print(f"Total for {month_name}: ${sum_month_expenses(args.month)}")
                else:
                    print(f"Not expenses in {month_name}")
        else:
            if not sum_expenses():
                print("Not expense for sum")
            else:
                print(f"Total expenses: ${sum_expenses()}")

    elif args.command == "setbudget":
        if set_budget(args.month, args.amount):
            print("Set budget")
    elif args.command == "export":
        export_csv()


# True or false if amount < 0
def check_amount(amount: float):
    if amount < 0:
        print("Amount must be greater than 0")
        return False
    return True


# Create expense with desc amount cat
def create_expense(description: str, amount: float, category: str):
    if not check_amount(amount):
        return False

    return {
        "description": description.strip(),
        "category": category.strip(),
        "amount": amount,
        "date": date.today().strftime("%Y-%m-%d"),
    }


def add_id(data: dict):
    if not data:
        return 1
    else:
        return data[len(data) - 1]["id"] + 1


# Add expense in dict with id,desc,amount,date in the json
def add_expense(expense: dict):
    new_expense = expense
    with open(EXPENSES_FILE) as expenses:
        data = json.load(expenses)

    # Create id
    new_expense["id"] = add_id(data)
    # Add expense
    data.append(new_expense)

    with open(EXPENSES_FILE, "w") as expenses:
        json.dump(data, expenses, indent=4)


# Delete expense by id
def delete_expense(id: int):
    with open(EXPENSES_FILE) as expenses:
        data = json.load(expenses)

        for expense in data:
            if expense["id"] == id:
                data.remove(expense)
                with open(EXPENSES_FILE, "w") as expenses:
                    json.dump(data, expenses, indent=4)
                    return True

        return False


# Update expenses by id
def update_expense(*args):
    id, desc, amount, category = args

    with open(EXPENSES_FILE, "r") as expenses:
        data = json.load(expenses)

    for expense in data:
        if expense["id"] == id:
            if desc is not None:
                expense["description"] = desc
            if amount is not None and check_amount(amount):
                expense["amount"] = amount
            else:
                return False
            if category is not None:
                expense["category"] = category.strip()

            with open(EXPENSES_FILE, "w") as expenses:
                json.dump(data, expenses, indent=4)
                return True

    return False


# View list the all expenses in json
def view_expenses():
    with open(EXPENSES_FILE) as expenses:
        data = json.load(expenses)
        if data:
            print(
                "{:<4}{:<13}{:<20}{:<10}{:<1}".format(
                    "ID", "Date", "Description", "Amount", "Category"
                )
            )
            for expense in data:
                print(
                    "{:<4}{:<13}{:<20}${:<10}{:<1}".format(
                        expense["id"],
                        expense["date"],
                        expense["description"],
                        expense["amount"],
                        expense["category"],
                    )
                )
        else:
            print("Not expenses in list")


# View expenses categorys
def view_expenses_cat(category: str):
    with open(EXPENSES_FILE) as expenses:
        data = json.load(expenses)
        expenses_cat = [expense for expense in data if expense["category"] == category]
        if expenses_cat:
            print(f"{category.title()} LIST:\n")
            print(
                "{:<4}{:<13}{:<20}{:<6}".format("ID", "Date", "Description", "Amount")
            )
            for expense in expenses_cat:
                print(
                    "{:<4}{:<13}{:<20}${:<6}".format(
                        expense["id"],
                        expense["date"],
                        expense["description"],
                        expense["amount"],
                    )
                )
        else:
            print(f"Not expenses in {category.title()}")


# Sum all amount expenses
def sum_expenses():
    with open(EXPENSES_FILE) as expenses:
        data = json.load(expenses)
        if data:
            return sum((expense["amount"] for expense in data))
        else:
            return False


def check_month(month: int):
    if month not in range(1, 13):
        print("Not is valid month")
        return False
    return month


# Sum month amount expenses
def sum_month_expenses(month: int):
    with open(EXPENSES_FILE) as expenses:
        data = json.load(expenses)
        dates_exp = (
            expense
            for expense in data
            if date.fromisoformat(expense["date"]).month == month
        )
        if dates_exp:

            # Sum expenses
            total_exp = sum(expense["amount"] for expense in dates_exp)
            check_budget(month, total_exp)
            return total_exp

    return False


def set_budget(month: int, budget: int):
    if budget > 0:

        month = str(month)
        with open(BUDGETS_FILE) as budgets:
            budgets_dict = json.load(budgets)
            budgets_dict[month] = budget

        with open(BUDGETS_FILE, "w") as budgets:
            json.dump(budgets_dict, budgets, indent=4)
            return True
    else:
        print("Budget must be greater than 0")
        return False


def check_budget(month: int, summary: float):
    month = str(month)
    with open(BUDGETS_FILE) as budgets:
        data = json.load(budgets)
        if data[month] != 0 and data[month] < summary:
            print(f"You went over the limit this month by ${summary-data[month]}")
            print(f"Limit is: ${data[month]}")


def export_csv():
    with open(EXPENSES_FILE) as expenses:
        data = json.load(expenses)

    if data:
        with open("expenses.csv", "w") as file:
            fieldnames = ["id", "description", "amount", "category", "date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            print("Create expenses.csv!")
            return True
    else:
        print("Not data for export")
        return False


if __name__ == "__main__":
    main()
