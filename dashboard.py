import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import datetime
from collections import defaultdict


class DashboardPage(tk.Frame):
    def __init__(self, parent, controller,manager):
        super().__init__(parent)
        self.controller = controller
        self.manager = manager

        style = ttk.Style(self)
        style.theme_use('clam')

        tk.Label(self, text="Dashboard", font=("Helvetica", 20, "bold"), bg="#2c2c2c", fg="white").pack(pady=10)

        self.balance_var = tk.StringVar()
        self.income_var = tk.StringVar()
        self.expense_var = tk.StringVar()

        info_frame = tk.Frame(self)
        info_frame.pack(pady=30)

        # Create individual cards for Balance, Income, Expenses
        balance_card = tk.Frame(info_frame, bg="#2c2c2c", padx=20, pady=10, width=150, height=80)
        income_card = tk.Frame(info_frame, bg="#2c2c2c", padx=20, pady=10, width=150, height=80)
        expense_card = tk.Frame(info_frame, bg="#2c2c2c", padx=20, pady=10, width=150, height=80)

        balance_card.grid(row=0, column=0, padx=15)
        income_card.grid(row=0, column=1, padx=15)
        expense_card.grid(row=0, column=2, padx=15)

        # Balance
        tk.Label(balance_card, text="Balance", font=("Helvetica", 12), fg="white", bg="#2c2c2c").pack()
        tk.Label(balance_card, textvariable=self.balance_var, font=("Helvetica", 16, "bold"), fg="white",
                 bg="#2c2c2c").pack()

        # Income
        tk.Label(income_card, text="Income", font=("Helvetica", 12), fg="lightgreen", bg="#2c2c2c").pack()
        tk.Label(income_card, textvariable=self.income_var, font=("Helvetica", 16, "bold"), fg="lightgreen",
                 bg="#2c2c2c").pack()

        # Expenses
        tk.Label(expense_card, text="Expenses", font=("Helvetica", 12), fg="salmon", bg="#2c2c2c").pack()
        tk.Label(expense_card, textvariable=self.expense_var, font=("Helvetica", 16, "bold"), fg="salmon",
                 bg="#2c2c2c").pack()

        self.chart_frame = tk.Frame(self,bg="#f0f0f0")
        self.chart_frame.pack(pady =20)

    def refresh(self):
        balance = self.manager.calc_balance()
        income = sum (t.amount for t in self.manager.transactions if t.amount > 0)
        expenses = sum (t.amount for t in self.manager.transactions if t.amount < 0)
        self.balance_var.set(f"${balance:.2f}")
        self.income_var.set(f"${income:.2f}")
        self.expense_var.set(f"${expenses:.2f}")
        self.plot_cashflow()

    def plot_cashflow(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        income_by_date = defaultdict(float)
        expenses_by_date = defaultdict(float)

        for t in self.manager.transactions:
            date = datetime.datetime.strptime(t.date, "%Y-%m-%d").date()
            if t.amount > 0:
                income_by_date[date] += t.amount
            else:
                expenses_by_date[date] += abs(t.amount)

        all_dates = sorted(set(income_by_date.keys()) | set(expenses_by_date.keys()))

        income_val = [income_by_date[date] for date in all_dates]
        expense_val = [expenses_by_date[date] for date in all_dates]

        fig, ax = plt.subplots(figsize=(7.5,4))
        ax.plot(all_dates, income_val, label="Income", marker='o', color='g')
        ax.plot(all_dates, expense_val, label="Expenses", marker='o', color='r')
        fig.autofmt_xdate(rotation=45)

        ax.set_title("Income vs Expenses", color = "white")
        ax.set_xlabel("Date", color = "white")
        ax.set_ylabel("Amount USD", color = "white")

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        ax.set_facecolor('#2c2c2c')
        fig.patch.set_facecolor('#2c2c2c')

        legend = ax.legend(facecolor="#2c2c2c", edgecolor="white")
        for text in legend.get_texts():
            text.set_color("white")


        ax.grid(visible=True, linestyle='--', alpha=0.6, color = "gray")

        canvas = FigureCanvasTkAgg(fig, master = self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
