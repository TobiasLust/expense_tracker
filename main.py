import json
import argparse
from datetime import date


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
        "-a", "--amount", type=int, required=True, help="Amount of the expense"
    )

    # "DELETE" COMMAND
    parser_delete = subparser.add_parser("delete", help="Delete expense by id=")
    parser_delete.add_argument(
        "--id", type=int, required=True, help="Id from expense Example: --id 1"
    )

    # "LIST" COMMAND
    parser_delete = subparser.add_parser("list", help="View all expenses")

    # Check command in cli
    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
        print("Expense added!")
    elif args.command == "list":
        view_expenses()


# Add expense in dict with id,desc,amount,date in the json
def add_expense(description, amount):

    with open("expenses.json", "r") as expenses:
        data = json.load(expenses)

    new_expense = {
        "id": len(data) + 1,
        "description": description,
        "amount": amount,
        "date": date.today().strftime("%Y-%m-%d"),
    }

    data.append(new_expense)

    with open("expenses.json", "w") as expenses:
        json.dump(data, expenses, indent=4)


def view_expenses():
    with open("expenses.json") as expenses:
        data = json.load(expenses)

        print("{:<4}{:<13}{:<20}{:<6}".format("ID", "Date", "Description", "Amount"))
        for expense in data:
            print(
                "{:<4}{:<13}{:<20}{:<6}".format(
                    expense["id"],
                    expense["date"],
                    expense["description"],
                    expense["amount"],
                )
            )


if __name__ == "__main__":
    main()
