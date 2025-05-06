# BudgetBud

BudgetBud is a simple personal budgeting app built with Python. It allows users to upload CSV files containing transaction data, categorize their expenses, and get a quick overview of their spending.

## Features

- Upload and parse CSV files of bank transactions
- Automatically categorize expenses using keyword matching
- Basic GUI (Tkinter) for file upload and interaction
- Object-oriented structure with `Transaction` class and budgeting logic

## How to Run

1. Make sure you have Python 3 and virtualenv installed.
2. Activate the virtual environment:
   ```bash
   source venv311/bin/activate  # Mac/Linux
   venv311\Scripts\activate     # Windows
3.
   ```bash
   pip install -r requirements.txt
   ```
   If requirements.txt does not exist, generate it with:
   ```bash
   pip freeze > requirements.txt
4. Run the app
   ```bash
   python main.py

