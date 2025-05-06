from transformers import pipeline

# Download once, then it's local
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def categorize_transaction(description):
    labels = ["Entertainment", "Food", "Utilities", "Housing", "Shopping", "Transportation", "Other"]
    result = classifier(description, labels)
    return result['labels'][0]

class Transaction:
    def __init__(self,date, description, amount):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = categorize_transaction(description) if amount < 0 else "Income"


    def __str__(self):
        return f"{self.date} | {self.description} | {self.category} | ${self.amount: .2f}"


"""
print("---Test Transactions Categorizer---")
print(f"Netflix Subscription -> {categorize_transaction('Netflix Subscription')}")
print(f"Water bill -> {categorize_transaction('Water bill')}")
print(f"In-n-Out Burger -> {categorize_transaction('In-n-Out Burger')}")
print(f"Rent -> {categorize_transaction('Rent')}")
print(f"Clothes -> {categorize_transaction('Clothes')}")
print(f"Bus ticket -> {categorize_transaction('Bus ticket')}")
print(f"Zombie Apocalypse Survival Gear -> {categorize_transaction('Zombie Apocalypse Survival Gear')}")
print("-------------Complete---------------")
"""