import tkinter as tk
import tkinter.ttk as ttk
from core.manager import BudgetManager


from gui.dashboard import DashboardPage
from gui.activity import ActivityPage
from gui.upload import UploadPage
from PIL import Image, ImageTk
import os

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.manager = BudgetManager()
        self.title("BudgetBud")
        self.geometry("1100x900")
        self.resizable(width=False, height=False)

        # navi bar at top
        self.navbar = tk.Frame(self, bg="#f0f0f0", height = 70)
        self.navbar.pack(side="top", fill="x")
        self.pages = {}


        logo_path = os.path.join(os.path.dirname(__file__),"logo.png")
        img = Image.open(logo_path).resize((50,50))
        self.logo = ImageTk.PhotoImage(img)
        tk.Label(self.navbar, image = self.logo, bg="#f0f0f0").pack(side="left", padx=10)



        for title in ["Dashboard", "Activity", "Upload"]:
            btn = ttk.Button(self.navbar, text = title ,command = lambda n = title: self.show_page(n))
            btn.pack(side="left", padx=10)

        #page containers
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        #init pages
        for PageClass in (DashboardPage, ActivityPage, UploadPage):
            page = PageClass(self.container, self, self.manager)
            self.pages[PageClass.__name__]= page
            page.grid(row=0, column=0, sticky="nsew")
        self.show_page("DashboardPage")

    def show_page(self, page_name):
        page_name += "Page" if not page_name.endswith("Page") else ""
        self.pages[page_name].tkraise()

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()