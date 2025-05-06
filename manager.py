import csv
from core.transaction import Transaction

class BudgetManager:
    def __init__(self):
        self.transactions=[]

    def load_transactions(self,filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                trans = Transaction(
                    row["Date"], row["Description"], float(row["Amount"])
                )
                self.transactions.append(trans)

    def calc_balance(self):
        return sum(trans.amount for trans in self.transactions)

    def costs_by_category(self):
        categories = {}
        for trans in self.transactions:
            if trans.amount <0 and trans.category != "Income":
                categories[trans.category] = categories.get(trans.category, 0) + trans.amount
        return categories


    def get_all_transactions(self):
        return self.transactions
