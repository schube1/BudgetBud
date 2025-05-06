
import tkinter as tk
from tkinter import filedialog, ttk
class UploadPage(tk.Frame):
    def __init__(self, parent, controller,manager):
        super().__init__(parent)
        self.controller = controller
        self.manager = manager



        tk.Label(self, text="Add Transactions", font=("Helvetica", 20, "bold"), fg="white").pack(pady=10)

        upload_button = tk.Button(self, text= "Upload CSV", command = self.upload_csv)
        upload_button.pack(pady =10)

    def upload_csv(self):
        filename = filedialog.askopenfilename(filetypes = [("CSV files", "*.csv")])
        if filename:
            self.manager.load_transactions(filename)

            print(f"Uploaded CSV file : {len(self.manager.transactions)} transactions")
            self.controller.pages["DashboardPage"].refresh()
            self.controller.pages["ActivityPage"].refresh()
