import tkinter as tk
from tkinter import ttk



class ActivityPage(tk.Frame):
    def __init__(self, parent, controller, manager):
        super().__init__(parent)
        self.controller = controller
        self.manager = manager

        tk.Label(self, text="Activity", font=("Helvetica", 20, "bold"), fg="white").pack(pady=10)

        # mian layout contain list and pie chart
        content_frame = tk.Frame(self)
        content_frame.pack(fill="both", expand=True)

        #transaciton list activity
        list_frame = tk.Frame(content_frame)
        list_frame.pack(side="left", fill="both", expand=True, padx=(30, 10))

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="left", fill="y")

        filter_frame = tk.Frame(list_frame)
        filter_frame.pack(fill="x", pady=(0, 10))

        self.category_var = tk.StringVar()
        tk.Entry(filter_frame, textvariable = self.category_var, font=("Helvetica", 10),width = 20).pack(side= "left", padx = (0, 5))

        tk.Button(filter_frame,
                  text = "Filter",
                  command =self.filter_transactions,
                  font =( "Helvetica", 10, "bold"),
                  bg ="#444",
                  ).pack(side = "left")
        tk.Button(filter_frame,
                  text="Clear",
                  command=self.clear_filter,
                  font=("Helvetica", 10, "bold"),
                  bg="#444",
                  ).pack(side="left", padx= (5,0))


        self.scroll_canvas = tk.Canvas(list_frame, highlightthickness=0, yscrollcommand=scrollbar.set, width=440, height=600)
        self.scroll_canvas.pack(side="right", fill="y")
        scrollbar.config(command=self.scroll_canvas.yview)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = tk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))

        #pie chart
        self.chart_frame = tk.Frame(content_frame)
        self.chart_frame.pack(side="right", padx=(10, 30), pady=10)
        self.chart_canvas = None

    def refresh(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

       # color coded and labels for each transaction
        for txn in reversed(self.manager.transactions):
            amount_color = "lightgreen" if txn.amount > 0 else "salmon1"
            sign = "+" if txn.amount > 0 else "-"
            text = f"{txn.date:<12} | {txn.description:<20.20} | {txn.category:<14.14} | {sign}${abs(txn.amount):.2f}"

            label = tk.Label(
                self.scroll_frame,
                text=text,
                font=("Courier New", 10, "bold"),
                fg="#2c2c2d",
                bg=amount_color,
                anchor="w",
                justify="left",
                padx=5
            )
            label.pack(fill="x", pady=1)

        # pie chart implementation
        from collections import defaultdict
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        category_totals = defaultdict(float)
        for txn in self.manager.transactions:
            if txn.amount < 0:
                category_totals[txn.category] += abs(txn.amount)

        if category_totals:
            fig, ax = plt.subplots(figsize=(5, 4.5))
            labels = list(category_totals.keys())
            sizes = list(category_totals.values())
            colors = plt.cm.Pastel1.colors[:len(labels)]

            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, autopct='%1.1f%%',
                startangle=140, colors=colors, textprops=dict(color="black")
            )

            for autotext in autotexts:
                autotext.set_color("black")

            for text in texts:
                text.set_color("white")

            ax.axis('equal')
            fig.patch.set_facecolor('#2c2c2c')
            fig.tight_layout(pad=2)

            self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.chart_canvas.draw()
            self.chart_canvas.get_tk_widget().pack()

            #summary per category
            summary_frame = tk.Frame(self.chart_frame, bd = 1, relief = "solid")
            summary_frame.pack(pady=(15, 0), padx = 10)

            header = tk.Label(
                summary_frame,
                text = "Spending Per Category",
                font=("Helvetica", 20, "bold"),
                fg= "white",
                pady=5
            )
            header.pack(anchor="w")

            for cat in labels:
                label = tk.Label(
                    summary_frame,
                    text=f"{cat:<20}${category_totals[cat]:.2f}",
                    font=("Courier New", 11, "bold"),
                    fg="white",
                    anchor="w",
                    justify="left",
                    padx=10
                )
                label.pack(anchor="w")

    def filter_transactions(self):
        category = self.category_var.get().strip().lower()
        if not category:
            return
        filtered = [trans for trans in self.manager.transactions if trans.category.lower() == category]
        self.show_transactions(filtered)

    def clear_filter(self):
        self.category_var.set("")
        self.refresh()

    def show_transactions(self,transactions):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        for trans in transactions:
            amount_color = "lightgreen" if trans.amount > 0 else "salmon1"
            sign = "+" if trans.amount > 0 else "-"
            text = f"{trans.date:<12} | {trans.description:<20.20} | {trans.category:<14.14} | {sign}${abs(trans.amount):.2f}"

            label = tk.Label(
                self.scroll_frame,
                text=text,
                font=("Courier New", 10, "bold"),
                fg="#2c2c2c",
                bg=amount_color,
                anchor="w",
                justify="left",
                padx=5
            )
            label.pack(fill="x", pady=1)
