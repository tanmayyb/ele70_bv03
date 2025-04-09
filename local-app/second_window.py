import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import shutil
import subprocess


import sys
import urllib.request
import numpy as np
import pandas as pd


# Added because GUI has no implementation for date selection
HARDCODED_DATES = {
    "fsa": ("202001", "202401"),
    "zonal": ("2020", "2024"),
}
MODELS = {0:'', 1: "XGBoost", 2: "LSTM"}
OUTPUT_DIR = './outputs'


# load the datasets API
api_url = 'https://raw.githubusercontent.com/tanmayyb/ele70_bv03/refs/heads/main/api/datasets.py'
exec(urllib.request.urlopen(api_url).read())


# load the metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error
def mean_absolute_percentage_error(y_true, y_pred):
    """Calculates MAPE given y_true and y_pred"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100




class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert("end", string)
        self.text_widget.see("end")  # auto-scroll

    def flush(self):
        pass  # Needed for compatibility


class SecondWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="light blue")
        self.root.title("Capstone Project BV03_w2")
        self.model_var = tk.IntVar()
        self.xgb_var = tk.IntVar(value=1)
        self.selected_file = ""

        self.ieso_dataset = None

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        tk.Label(self.root, text="Software Name: Forecaster", font=("Times New Roman", 40, "bold"), bg="yellow", fg="black", height=2).pack(fill=tk.X, pady=(50, 0))

        tk.Label(self.root, text="Select FSA or Zonal", font=("Times New Roman", 12, "bold"), bg="light blue").place(x=400, y=648)
        tk.Label(self.root, text="Select a Zone or a City", font=("Times New Roman", 12, "bold"), bg="light blue").place(x=400, y=798)
        tk.Label(self.root, text="OPTION_1_Loading your data: user the Search button to access your data, then the button Load to load it", font=("Times New Roman", 20, "bold"), bg="light blue").place(x=65, y=270)
        tk.Label(self.root, text="OPTION_2_Selection: Select data from recording station", font=("Times New Roman", 20, "bold"), bg="light blue").place(x=65, y=520)
        tk.Label(self.root, text="After using OPTION_1 or OPTION_2", font=("Times New Roman", 20, "bold"), bg="light blue").place(x=850, y=355)
        tk.Label(self.root, text="Select one Modules ---------------------------->", font=("Times New Roman", 20, "bold"), bg="light blue").place(x=850, y=395)
        tk.Label(self.root, text="Then clik on the Training button below", font=("Times New Roman", 20, "bold"), bg="light blue").place(x=850, y=435)

        tk.Label(self.root, text="SELECT DATASET", font=("Times New Roman", 12, "bold"), bg="light gray", width=30, height=2, relief="solid").place(x=200, y=570)
        self.search_entry = tk.Entry(self.root, font=("Times New Roman", 16), width=120)
        self.search_entry.place(x=70, y=230, height=40)

        self.energy_options = ["fsa", "zonal"]
        self.target_zone_options = []
        tk.Label(self.root, text="SELECT ENERGY REPOSITORY", font=("Times New Roman", 12, "bold"), bg="light green", width=30, height=2, relief="solid").place(x=100, y=650)
        self.energy_combobox = ttk.Combobox(self.root, values=self.energy_options, state="readonly", width=60)
        self.energy_combobox.place(x=400, y=675)
        self.energy_combobox.bind("<<ComboboxSelected>>", self.update_target_zones)

        tk.Label(self.root, text="SELECT TARGET ZONE", font=("Times New Roman", 12, "bold"), bg="light green", width=30, height=2, relief="solid").place(x=100, y=800)
        self.target_zone_combobox = ttk.Combobox(self.root, values=self.target_zone_options, state="readonly", width=60)
        self.target_zone_combobox.place(x=400, y=825)
        self.target_zone_combobox.bind("<<ComboboxSelected>>", self.load_dataset_on_zone_selection)

        tk.Button(self.root, text="Search", font=("Times New Roman", 16, "bold"), bg="light green", width=15, command=self.search_csv_file).place(x=1450, y=230)
        tk.Button(self.root, text="Load", font=("Times New Roman", 16, "bold"), bg="sky blue", width=10, command=self.load_csv_file).place(x=1700, y=230)

        self.evolution_frame = tk.Frame(self.root, bg="light gray", width=900, height=400)
        self.evolution_frame.place(x=900, y=550)
        tk.Label(self.evolution_frame, text="Evolution of data training and analysis", font=("Times New Roman", 20, "bold"), bg="light gray").place(x=200, y=30)
        self.evolution_text = tk.Text(self.evolution_frame, font=("Times New Roman", 12), bg="white", fg="black", width=95, height=15)
        self.evolution_text.place(x=50, y=80)

        module_frame = tk.Frame(self.root, bg="white", width=500, height=200)
        module_frame.place(x=1350, y=325)
        tk.Label(module_frame, text="Modules", font=("Times New Roman", 30, "bold"), bg="white").place(x=150, y=30, anchor="center")

        tk.Radiobutton(module_frame, variable=self.model_var, value=1, bg="white").place(x=30, y=75)
        tk.Label(module_frame, text="XGBoost Model: eXtr Grad Boost", font=("Times New Roman", 22), bg="white").place(x=70, y=75)

        tk.Radiobutton(module_frame, variable=self.model_var, value=2, bg="white").place(x=30, y=125)
        tk.Label(module_frame, text="LSTM: Long Short Term Memory", font=("Times New Roman", 22), bg="white").place(x=70, y=125)

        tk.Button(self.root, text="  Training & Analysis ", font=("Times New Roman", 22, "bold"), bg="light green", width=22, command=self.run_training).place(x=900, y=480)
        tk.Button(self.root, text="  Run For Anomaly ", font=("Times New Roman", 22, "bold"), bg="red", width=22, command=self.run_anomaly_detection).place(x=900, y=980)
        tk.Button(self.root, text="BACK", font=("Times New Roman", 20, "bold"), bg="light green", width=17, command=self.go_back).place(x=75, y=980)
        tk.Button(self.root, text="End Presentation", font=("Times New Roman", 22, "bold"), bg="orange", command=self.end_presentation).place(x=1550, y=980)

        sys.stdout = TextRedirector(self.evolution_text)

    def update_target_zones(self, event):
        selected_energy = self.energy_combobox.get()
        if selected_energy == "fsa":
            self.ieso_dataset = IESODataset('fsa')
        elif selected_energy == "zonal":
            self.ieso_dataset = IESODataset('zonal')

        self.selected_dates = HARDCODED_DATES[selected_energy] # choose the dates based on the energy type
        # self.available_dates = self.ieso_dataset.get_dates() # not implemented in the GUI
        self.target_zone_options = self.ieso_dataset.get_target_options()
        self.target_zone_combobox["values"] = self.target_zone_options
        self.target_zone_id = {zone: i for i, zone in enumerate(self.target_zone_options)}
        self.target_zone_combobox.set("")


    def search_csv_file(self):
        folder_path = r"C:\Users\OWNER\Desktop\CAPSTONE PROJECT\AccessFiles\offline"
        file_path = filedialog.askopenfilename(
            initialdir=folder_path,
            title="Select CSV File",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if file_path:
            self.selected_file = file_path
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, file_path)

    def load_csv_file(self):
        if self.selected_file:

            msg = f"Loading Dataset:\n"
            msg += f"File Path: {self.selected_file}\n"
            self.evolution_text.insert(tk.END, msg)
            self.evolution_text.update()

            # functionally equivalent to the load_dataset_on_zone_selection function
            target_name, dataset, dt = DatasetPreprocessor.load_dataset(self.selected_file)

            # set the target name, dataset, and dt
            self.target_name = target_name
            self.dataset = dataset
            self.dt = dt

            # update text
            msg = f"...Dataset loaded successfully!\n"
            self.evolution_text.insert(tk.END, msg)
            self.evolution_text.update()
            self.evolution_text.see("end")
        else:
            messagebox.showwarning("Warning", "Please select a CSV file first using Search.")


    def load_dataset_on_zone_selection(self, event):
        target_zone = self.target_zone_combobox.get()
        target_zone_id = self.target_zone_id[target_zone]        

        # update text
        msg = f"Loading Dataset:\n"
        msg += f"Target Zone: {target_zone}\n"
        msg += f"Start Date: {self.selected_dates[0]}\n"
        msg += f"End Date: {self.selected_dates[1]}...\n"
        self.evolution_text.insert(tk.END, msg)
        self.evolution_text.update()

        # Load the dataset using user selections
        self.ieso_dataset.set_target(target_zone_id)
        self.ieso_dataset.load_dataset(start_date=self.selected_dates[0], end_date=self.selected_dates[1], download=True)
        self.climate = ClimateDataset(self.ieso_dataset)
        self.climate.load_dataset(sample_num=5, download=True)
        self.preprocessor = DatasetPreprocessor(self.ieso_dataset, self.climate)
        target_name, dataset, dt = self.preprocessor.preprocess()

        # set the target name, dataset, and dt
        self.target_name = target_name
        self.dataset = dataset
        self.dt = dt

        # update text
        msg = f"...Dataset loaded successfully!\n"
        self.evolution_text.insert(tk.END, msg)
        self.evolution_text.update()
        self.evolution_text.see("end")


    def run_training(self):
        # Create train and test sets
        (X_train, X_test, y_train, y_test), (train_idx, test_idx) = create_train_test_split(self.dataset, target=self.target_name, dt=self.dt)
        y_test_numpy = y_test.to_numpy()

        model_selected = self.model_var.get()
        model_name = MODELS[model_selected]

        # notify on training start
        self.evolution_text.insert(tk.END, f"Model selected: {model_name}\n")
        self.evolution_text.insert(tk.END, f"Training...\n")
        self.evolution_text.update()
        try:
            if model_selected == 1:
                from models.xgboost import xgb_train
                pred, output_df = xgb_train(X_train, y_train, X_test, y_test, self.dt)

            elif model_selected == 2:
                from models.lstm import lstm_train
                pred, output_df = lstm_train(X_train, y_train, X_test, y_test, self.dataset, self.dt)
            else:
                raise ValueError(f"Invalid model selected: {model_selected}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        self.output_df = output_df

        # update text on finishing training 
        self.evolution_text.insert(tk.END, f"...Training complete!\n")
        self.evolution_text.update()
        self.evolution_text.see("end")

        # calculate statistics
        mse = mean_squared_error(y_test, pred)
        mae = mean_absolute_error(y_test, pred)
        mape = mean_absolute_percentage_error(y_test, pred)

        # update text on calculating statistics
        self.evolution_text.insert(tk.END, f"Model Performance Statistics:\n")
        self.evolution_text.insert(tk.END, f"MSE: {mse}\n")
        self.evolution_text.insert(tk.END, f"MAE: {mae}\n")
        self.evolution_text.insert(tk.END, f"MAPE: {mape}\n")
        self.evolution_text.update()
        self.evolution_text.see("end")


        # plot prediction
        from plotly import graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scattergl(
            x=test_idx,
            y=y_test.to_numpy(),
            name='Actual',
            line_color='blue')
        )
        fig.add_trace(go.Scattergl(
            x=test_idx,
            y=pred,
            name='Predicted',
            line_color='red')
        )
        # Set the theme to 'plotly_white'
        fig.update_layout(
            title=f"Time Series Forecasting for {self.target_name} with {model_name}",
            xaxis_title="t (1 unit = 1 hour)",
            yaxis_title="Energy Demand",
            template="plotly_white",
            xaxis = dict( rangeslider=dict(
            visible=True
            ))
        )
        fig.show()

    def run_anomaly_detection(self):
        try:
            from models.anomaly_detection import AnomalyDetection
            anomaly_detection = AnomalyDetection(self.output_df, self.target_name)

            # plot the summary plots
            anomaly_detection.summary_plots()
            anomaly_detection.num_anomalies()
            anomaly_detection.best_ten_anomalies()
            anomaly_detection.worst_ten_anomalies()
            anomaly_detection.anomalies_per_day()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def end_presentation(self):
        self.root.destroy()

    def go_back(self):
        from first_window import FirstWindow
        self.root.destroy()
        FirstWindow()

    def display_message(self, message):
        messagebox.showinfo("Message", message)

if __name__ == "__main__":
    SecondWindow()
