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

    # "LIST" COMMAND
    parser_delete = subparser.add_parser("list", help="View all expenses")

    # Check command in cli
    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
        print("Expense added!")
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount)
    elif args.command == "list":
        view_expenses()


# Add expense in dict with id,desc,amount,date in the json
def add_expense(description, amount):

    with open("expenses.json") as expenses:
        data = json.load(expenses)

    new_expense = {
        "id": len(data) + 1,
        "description": description.strip(),
        "amount": amount,
        "date": date.today().strftime("%Y-%m-%d"),
    }

    data.append(new_expense)

    with open("expenses.json", "w") as expenses:
        json.dump(data, expenses, indent=4)


# Delete expense by id
def delete_expense(id: int):
    with open("expenses.json") as expenses:
        data = json.load(expenses)

        for expense in data:
            if expense["id"] == id:
                data.remove(expense)
                with open("expenses.json", "w") as expenses:
                    json.dump(data, expenses, indent=4)
                    print("Expense delete!")
                    return

        print("ID not found")


def update_expense(*args):
    id, desc, amount = args
    with open("expenses.json", "r") as expenses:
        data = json.load(expenses)

    for expense in data:
        if expense["id"] == id:
            if desc is not None:
                expense["description"] = desc
            if amount is not None:
                expense["amount"] = amount

            with open("expenses.json", "w") as expenses:
                json.dump(data, expenses, indent=4)
            print("Expense Updated!")
            return

    print("ID does not exist!")


# View list the all expenses in json
def view_expenses():
    with open("expenses.json") as expenses:
        data = json.load(expenses)

        print("{:<4}{:<13}{:<20}{:<6}".format("ID", "Date", "Description", "Amount"))
        for expense in data:
            print(
                "{:<4}{:<13}{:<20}${:<6}".format(
                    expense["id"],
                    expense["date"],
                    expense["description"],
                    expense["amount"],
                )
            )


if __name__ == "__main__":
    main()
