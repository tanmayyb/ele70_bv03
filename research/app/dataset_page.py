import tkinter as tk
from tkinter import ttk, messagebox

class DatasetChoicePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="DATASET CHOICE", font=("Helvetica", 24)).pack(pady=20)

        tk.Button(self, text="Load Datasets as CSV", command=lambda: controller.show_page("DatasetLoadPage")) \
            .pack(pady=10)

        tk.Button(self, text="Create New Datasets", command=lambda: controller.show_page("DatasetCreatePage")) \
            .pack(pady=10)


class DatasetLoadPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="LOAD DATASETS FROM CSV", font=("Helvetica", 24)).pack(pady=20)

        tk.Button(self, text="Load Dataset #1").pack(pady=10)
        tk.Button(self, text="Load Dataset #2").pack(pady=10)
        tk.Button(self, text="Back", command=lambda: controller.show_page("DatasetChoicePage")) \
            .pack(pady=10)


class DatasetCreatePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="CREATE DATASET", font=("Helvetica", 24)).pack(pady=20)

        tk.Label(self, text="Select Weather Repository:").pack(pady=5)
        self.weather_repo = ttk.Combobox(self, values=["Repo 1", "Repo 2", "Repo 3"])
        self.weather_repo.pack(pady=5)

        tk.Label(self, text="Select Zone:").pack(pady=5)
        self.zone = ttk.Combobox(self, values=["Zone 1", "Zone 2", "Zone 3"])
        self.zone.pack(pady=5)

        tk.Label(self, text="Select Energy Repository:").pack(pady=5)
        self.energy_repo = ttk.Combobox(self, values=["Energy Repo 1", "Energy Repo 2", "Energy Repo 3"])
        self.energy_repo.pack(pady=5)

        tk.Button(self, text="Create Dataset", command=self.create_dataset).pack(pady=20)
        tk.Button(self, text="Back", command=lambda: controller.show_page("DatasetChoicePage")) \
            .pack(pady=10)

    def create_dataset(self):
        weather = self.weather_repo.get()
        zone = self.zone.get()
        energy = self.energy_repo.get()

        if not weather or not zone or not energy:
            messagebox.showerror("Error", "Please fill all fields to create a dataset.")
        else:
            messagebox.showinfo("Success", f"Dataset created with {weather}, {zone}, {energy}.")
            self.controller.show_page("TrainingDashboard")  # Navigate to TrainingDashboard after success


if __name__ == "__main__":
    # Create a test window to host our frames
    root = tk.Tk()
    root.title("Dataset Pages Test")
    root.geometry("800x600")
    root.resizable(False, False)
    
    # Simple controller class to handle page switching
    class TestController:
        def __init__(self, container):
            self.container = container
            self.pages = {}
            
            # Initialize all pages
            for Page in (DatasetChoicePage, DatasetLoadPage, DatasetCreatePage):
                page = Page(container, self)
                self.pages[Page.__name__] = page
                page.grid(row=0, column=0, sticky="nsew")
            
            # Show initial page
            self.show_page("DatasetChoicePage")
        
        def show_page(self, page_name):
            page = self.pages[page_name]
            page.tkraise()
    
    # Create and run the test application
    controller = TestController(root)
    root.mainloop()