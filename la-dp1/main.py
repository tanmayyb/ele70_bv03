import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page Application")
        self.geometry("800x600")
        self.resizable(False, False)

        # Container for all pages
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.pages = {}

        for Page in (LoginPage, DatasetChoicePage, DatasetLoadPage, DatasetCreatePage, TrainingDashboard, AnalysisDashboard):
            page = Page(parent=self.container, controller=self)
            self.pages[Page.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("LoginPage")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="APP TITLE", font=("Helvetica", 24)).pack(pady=20)
        
        tk.Label(self, text="USERNAME").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="PASSWORD").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=lambda: controller.show_page("DatasetChoicePage")) \
            .pack(pady=20)


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

        from tkinter import messagebox
        if not weather or not zone or not energy:
            messagebox.showerror("Error", "Please fill all fields to create a dataset.")
        else:
            messagebox.showinfo("Success", f"Dataset created with {weather}, {zone}, {energy}.")
            self.controller.show_page("TrainingDashboard")  # Navigate to TrainingDashboard after success


class TrainingDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Training Dashboard: Configuration", font=("Helvetica", 24)).pack(pady=20)

        # Model selection frame
        model_frame = ttk.LabelFrame(self, text="Select Models to Train")
        model_frame.pack(pady=10, padx=20, fill="x")

        # Checkboxes for model selection
        self.train_xgboost = tk.BooleanVar(value=True)
        self.train_arima = tk.BooleanVar(value=True)

        # XGBoost section
        xgboost_frame = ttk.Frame(model_frame)
        xgboost_frame.pack(fill="x", pady=5, padx=5)
        ttk.Checkbutton(xgboost_frame, text="Model 1: XGBoost", variable=self.train_xgboost).pack(side="left")
        tk.Button(xgboost_frame, text="Configure", command=self.open_xgboost_config).pack(side="right")

        # ARIMA section
        arima_frame = ttk.Frame(model_frame)
        arima_frame.pack(fill="x", pady=5, padx=5)
        ttk.Checkbutton(arima_frame, text="Model 2: ARIMA", variable=self.train_arima).pack(side="left")
        tk.Button(arima_frame, text="Configure", command=self.open_arima_config).pack(side="right")

        # Navigation buttons
        tk.Button(self, text="Train Selected Models", command=self.train_models).pack(pady=20)
        tk.Button(self, text="Back", command=lambda: controller.show_page("DatasetChoicePage")) \
            .pack(pady=5)

    def train_models(self):
        if not self.train_xgboost.get() and not self.train_arima.get():
            messagebox.showerror("Error", "Please select at least one model to train.")
            return
        self.controller.show_page("AnalysisDashboard")

    def open_xgboost_config(self):
        config_window = tk.Toplevel(self)
        config_window.title("XGBoost Configuration")
        config_window.geometry("400x500")
        config_window.resizable(False, False)

        # Create a main frame with scrollbar
        main_frame = ttk.Frame(config_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add parameters
        tk.Label(main_frame, text="Learning Rate:").pack(anchor="w", pady=5)
        learning_rate = ttk.Scale(main_frame, from_=0.01, to=1.0, orient="horizontal")
        learning_rate.set(0.1)
        learning_rate.pack(fill="x", pady=5)
        
        tk.Label(main_frame, text="Max Depth:").pack(anchor="w", pady=5)
        max_depth = ttk.Spinbox(main_frame, from_=1, to=15, width=10)
        max_depth.set(6)
        max_depth.pack(anchor="w", pady=5)

        tk.Label(main_frame, text="N Estimators:").pack(anchor="w", pady=5)
        n_estimators = ttk.Spinbox(main_frame, from_=50, to=1000, increment=50, width=10)
        n_estimators.set(100)
        n_estimators.pack(anchor="w", pady=5)

        tk.Label(main_frame, text="Min Child Weight:").pack(anchor="w", pady=5)
        min_child_weight = ttk.Spinbox(main_frame, from_=1, to=10, width=10)
        min_child_weight.set(1)
        min_child_weight.pack(anchor="w", pady=5)

        tk.Label(main_frame, text="Subsample:").pack(anchor="w", pady=5)
        subsample = ttk.Scale(main_frame, from_=0.1, to=1.0, orient="horizontal")
        subsample.set(1.0)
        subsample.pack(fill="x", pady=5)

        # Buttons frame
        button_frame = ttk.Frame(config_window)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(button_frame, text="Save", command=config_window.destroy).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancel", command=config_window.destroy).pack(side="right", padx=5)

    def open_arima_config(self):
        config_window = tk.Toplevel(self)
        config_window.title("ARIMA Configuration")
        config_window.geometry("400x400")
        config_window.resizable(False, False)

        # Create a main frame
        main_frame = ttk.Frame(config_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add parameters
        tk.Label(main_frame, text="p (AR order):").pack(anchor="w", pady=5)
        p_order = ttk.Spinbox(main_frame, from_=0, to=10, width=10)
        p_order.set(1)
        p_order.pack(anchor="w", pady=5)

        tk.Label(main_frame, text="d (Difference order):").pack(anchor="w", pady=5)
        d_order = ttk.Spinbox(main_frame, from_=0, to=2, width=10)
        d_order.set(1)
        d_order.pack(anchor="w", pady=5)

        tk.Label(main_frame, text="q (MA order):").pack(anchor="w", pady=5)
        q_order = ttk.Spinbox(main_frame, from_=0, to=10, width=10)
        q_order.set(1)
        q_order.pack(anchor="w", pady=5)

        tk.Label(main_frame, text="Seasonal Order (m):").pack(anchor="w", pady=5)
        seasonal = ttk.Spinbox(main_frame, from_=0, to=24, width=10)
        seasonal.set(12)
        seasonal.pack(anchor="w", pady=5)

        # Buttons frame
        button_frame = ttk.Frame(config_window)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(button_frame, text="Save", command=config_window.destroy).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancel", command=config_window.destroy).pack(side="right", padx=5)


class AnalysisDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Analysis Dashboard", font=("Helvetica", 24)).pack(pady=20)

        tk.Label(self, text="Loss Curve of Model #1").pack(pady=10)
        tk.Label(self, text="Plot of Test Predictions for Model #2").pack(pady=10)

        tk.Button(self, text="Finish", command=self.quit).pack(pady=20)
        tk.Button(self, text="Back", command=lambda: controller.show_page("TrainingDashboard")) \
            .pack(pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
