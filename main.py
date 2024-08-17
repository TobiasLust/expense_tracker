import json
import argparse
import calendar
import csv
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
        "-c",
        "--category",
        type=str,
        required=False,
        choices= ["housing","groceries","transportation","healthcare","entertainment","savings","clothing","others"],
        default= "Others",
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
        choices= ["housing","groceries","transportation","healthcare","entertainment","savings","clothing","others"],
        default= "Others",
        help="Category of expense",
    )

    # "LIST" COMMAND
    parser_list = subparser.add_parser("list", help="View all expenses")
    parser_list.add_argument(
        "-c", "--category", type=str, required=False,choices= ["housing","groceries","transportation","healthcare","entertainment","savings","clothing","others"], help="Amount of the expense"
    )
    

    # "SUMMARY" COMMAND
    parser_summary = subparser.add_parser(
        "summary", help="Summary all the expenses amount")
    parser_summary.add_argument("--month",type=int,required=False,help="Summary only month expenses")
    
    # "SET BUDGET" COMMAND
    parser_setbudget = subparser.add_parser("setbudget",help="Set budget for month expenses")
    parser_setbudget.add_argument("--month",type=int,choices=range(1,13),required=True,help="Month for set budget")
    parser_setbudget.add_argument("-a","--amount",type=int,required=True,help="Amount for set budget")
    
    # "EXPORT" COMMAND
    parser_export = subparser.add_parser("export", help="Export expenses to csv")

    # Check command in cli
    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount,args.category.strip())
        print("Expense added!")
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount,args.category)
    elif args.command == "list":
        if args.category:
            view_expenses_cat(args.category.strip())
        else:
            view_expenses()
    elif args.command == "summary":
        if args.month == 0 or args.month:
            sum_month_expenses(args.month)   
        else:
            sum_expenses()
    elif args.command == "setbudget":
        set_budget(args.month,args.amount)
    elif args.command == "export":
        export_csv()
        


# Add expense in dict with id,desc,amount,date in the json
def add_expense(description, amount,category):
    if amount < 0:
        print("Amount it has to be more than 0")

    with open("expenses.json") as expenses:
        data = json.load(expenses)

    new_expense = {
        "description": description.strip(),
        "category": category.title(),
        "amount": amount,
        "date": date.today().strftime("%Y-%m-%d"),
    }
    if not data:
        new_expense["id"] = 1
    else:
        new_expense["id"] = data[len(data)-1]["id"] + 1
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

# Update expenses by id
def update_expense(*args):
    id, desc, amount,category = args
    if amount < 0:
        print("Amount it has to be more than 0")
        return
    with open("expenses.json", "r") as expenses:
        data = json.load(expenses)

    for expense in data:
        if expense["id"] == id:
            if desc is not None:
                expense["description"] = desc
            if amount is not None:
                expense["amount"] = amount
            if category is not None:
                expense["category"] = category.title()

            with open("expenses.json", "w") as expenses:
                json.dump(data, expenses, indent=4)
            print("Expense Updated!")
            return

    print("ID does not exist!")


# View list the all expenses in json
def view_expenses():
    with open("expenses.json") as expenses:
        data = json.load(expenses)

        print("{:<4}{:<13}{:<20}{:<10}{:<1}".format("ID", "Date", "Description", "Amount","Category"))
        for expense in data:
            print(
                "{:<4}{:<13}{:<20}${:<10}{:<1}".format(
                    expense["id"],
                    expense["date"],
                    expense["description"],
                    expense["amount"],
                    expense["category"]
                )
            )
# View expenses categorys
def view_expenses_cat(category):
    category = category.title()
    with open("expenses.json") as expenses:
        data = json.load(expenses)
        expenses_cat = (expense for expense in data if expense["category"] == category)
        print(f"{category} LIST:\n")
        print("{:<4}{:<13}{:<20}{:<6}".format("ID", "Date", "Description", "Amount"))
        for expense in expenses_cat:
            print(
                "{:<4}{:<13}{:<20}${:<6}".format(
                    expense["id"],
                    expense["date"],
                    expense["description"],
                    expense["amount"],
                )
            )

# Sum all amount expenses
def sum_expenses():
    with open("expenses.json") as expenses:
        data = json.load(expenses)
        print(f"Total expenses: ${sum((expense["amount"] for expense in data))}")


# Sum month amount expenses
def sum_month_expenses(month):
    # Check valid month
    if month in range(1,13):
        
        # Get month from calendar
        month_name = calendar.month_name[month]
   
         
        with open("expenses.json") as expenses:
            data = json.load(expenses)
            dates_exp = (expense for expense in data if date.fromisoformat(expense["date"]).month == month)
            
            # Sum expenses
            total_exp = sum(expense["amount"] for expense in dates_exp)
            
            if total_exp > 0:
                print(f"Total expenses for {month_name}: ${total_exp}")
                check_budget(month,total_exp)
            else:
                print(f"No expenses in {month_name}!")
    else:
        print(f"{month} not is valid month!")

def set_budget(month:int,budget:int):
    month = str(month)
    with open("budgets.json") as budgets:
            budgets_dict = json.load(budgets)
            budgets_dict[month] = budget
            print("Budget added!")
    with open("budgets.json","w") as budgets:
        json.dump(budgets_dict,budgets,indent=4)

def check_budget(month,summary):
    month = str(month)
    with open("budgets.json") as budgets:
        data = json.load(budgets)
        if data[month] != 0 and  data[month] < summary:
            print(f"You went over the limit this month by ${summary-data[month]}")
            print(f"Limit is: ${data[month]}")

 
def export_csv():
    with open("expenses.json") as expenses:
            data = json.load(expenses)
            
    if data:
        with open("expenses.csv","w") as file:
            fieldnames = ["id","description","amount","category","date"]
            writer = csv.DictWriter(file,fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            print("Create expenses.csv!")
    else:
        print("Expenses empty!")
        
    


if __name__ == "__main__":
    main()
