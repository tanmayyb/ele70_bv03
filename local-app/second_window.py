import tkinter as tk
import threading
import time
import subprocess
import pandas as pd
from third_window import ThirdWindow

class SecondWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="light blue")
        self.root.title("Capstone Project BV03_w2")
        self.data_frame_normal = pd.read_csv(r"C:\Users\OWNER\Desktop\Year 6\Winter 2024\ELE 70B\Presentation2\NormalToPrediction_1.csv")
        self.data_frame_anormal = pd.read_csv(r"C:\Users\OWNER\Desktop\Year 6\Winter 2024\ELE 70B\Presentation2\AnormalToPrediction_1.csv")
        self.normal_row_index = 0
        self.anormal_row_index = 0
        self.progress_label = None
        self.csv_selection = None
        self.model_selection = None
        self.date_time_box = None
        self.real_value_box = None
        self.predict_value_box = None
        self.differ_box = None
        self.adate_time_box = None
        self.areal_value_box = None
        self.apredict_value_box = None
        self.adiffer_box = None
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        tk.Label(self.root, text="Software Name: Forecaster", font=("Times New Roman", 40, "bold"), bg="yellow", fg="black", height=2).pack(fill=tk.X, pady=(50, 0))
        self.csv_selection = ThirdWindow.add_project_directory_box(self.root)
        self.model_selection = ThirdWindow.add_modules_box(self.root)
        self.progress_label = ThirdWindow.add_progress_box(self.root)
        self.date_time_box = ThirdWindow.add_date_time_box(self.root)
        self.real_value_box = ThirdWindow.add_real_value_box(self.root)
        self.predict_value_box = ThirdWindow.add_predict_value_box(self.root)
        self.differ_box = ThirdWindow.add_differ_box(self.root)
        self.adate_time_box = ThirdWindow.add_adate_time_box(self.root)
        self.areal_value_box = ThirdWindow.add_areal_value_box(self.root)
        self.apredict_value_box = ThirdWindow.add_apredict_value_box(self.root)
        self.adiffer_box = ThirdWindow.add_adiffer_box(self.root)

        tk.Button(self.root, text="Training", font=("Times New Roman", 20, "bold"), bg="red", fg="white", width=10, height=2, command=self.start_training).place(x=170, y=670)
        tk.Button(self.root, text="Analysis", font=("Times New Roman", 20, "bold"), bg="blue", fg="white", width=10, height=2, command=self.start_analysis).place(x=350, y=670)
        tk.Button(self.root, text="Normal Values Following Prediction", font=("Times New Roman", 18, "bold"), bg="green", fg="white", width=30, height=2, command=self.display_next_normal_row).place(x=1250, y=225)
        tk.Button(self.root, text="Anormal Values Following Prediction", font=("Times New Roman", 18, "bold"), bg="orange", fg="white", width=30, height=2, command=self.display_next_anormal_row).place(x=1250, y=580)
        tk.Button(self.root, text="\u2b05 Welcome Page", font=("Times New Roman", 22, "bold"), bg="green", fg="black", width=20, height=2, command=self.open_welcome_page).place(x=400, y=920)
        tk.Button(self.root, text="Graphic Representation \u27a1", font=("Times New Roman", 22, "bold"), bg="orange", fg="black", width=25, height=2, command=self.open_graphic_representation).place(x=1200, y=920)

        # Step Labels
        for step, x_pos, y_pos in [
            ("1st step", 0.03, 0.25), ("2cd step", 0.03, 0.45), ("3rd step", 0.09, 0.595), ("4th step", 0.19, 0.595), 
            ("5th step", 0.09, 0.75), ("6th step", 0.61, 0.22), ("7th step", 0.61, 0.55), ("8th step", 0.585, 0.875)
        ]:
            tk.Label(self.root, text=step, font=("Times New Roman", 14, "bold"), bg="light blue", fg="black").place(relx=x_pos, rely=y_pos)

    def start_training(self):
        threading.Thread(target=self.training_sequence).start()

    def training_sequence(self):
        time.sleep(3)
        self.run_model()
        for progress in range(10, 101, 3):
            self.progress_label.config(text=f"{progress} %")
            time.sleep(1)
        time.sleep(3)
        self.progress_label.config(text="Completed")

    def start_analysis(self):
        threading.Thread(target=self.analysis_sequence).start()

    def analysis_sequence(self):
        time.sleep(2)
        self.progress_label.config(text="0.00 %")
        for progress in range(10, 101, 10):
            time.sleep(1)
            self.progress_label.config(text=f"{progress} %")
        subprocess.run(["python", "C:\\Users\\OWNER\\Desktop\\Year 6\\Winter 2024\\ELE 70B\\Presentation2\\CodeForCSVFileNormalAnormal_1.py"])
        time.sleep(2)
        self.progress_label.config(text="Completed")

    def run_model(self):
        csv_selection = self.csv_selection.get()
        model_selection = self.model_selection.get()

        if csv_selection == "CSV file 1" and model_selection == "XGBoost Model:eXtr Grad Boost":
            subprocess.run(["python", "C:\\Users\\OWNER\\Desktop\\Year 6\\Winter 2024\\ELE 70B\\Presentation2\\XGboost\\CodeForTraningXGboostData1.py"])
        elif csv_selection == "CSV file 2" and model_selection == "XGBoost Model:eXtr Grad Boost":
            subprocess.run(["python", "C:\\Users\\OWNER\\Desktop\\Year 6\\Winter 2024\\ELE 70B\\Presentation2\\XGboost\\CodeForTraningXGboostData2.py"])
        elif csv_selection == "CSV file 1" and model_selection == "ARIMA Model:Auto Int Mov Aver":
            subprocess.run(["python", "C:\\Users\\OWNER\\Desktop\\Year 6\\Winter 2024\\ELE 70B\\Presentation2\\ArimaCode\\CodeForTraningArimaData1.py"])
        elif csv_selection == "CSV file 2" and model_selection == "ARIMA Model:Auto Int Mov Aver":
            subprocess.run(["python", "C:\\Users\\OWNER\\Desktop\\Year 6\\Winter 2024\\ELE 70B\\Presentation2\\ArimaCode\\CodeForTraningArimaData2.py"])

    def display_next_normal_row(self):
        if self.normal_row_index < len(self.data_frame_normal):
            row = self.data_frame_normal.iloc[self.normal_row_index]
            self.date_time_box.config(text=row['DateTime'])
            self.real_value_box.config(text=row['Toronto'])
            self.predict_value_box.config(text=row['Predicted'])
            self.differ_box.config(text=row['Abs_Val_Err'])
            self.normal_row_index += 1

    def display_next_anormal_row(self):
        if self.anormal_row_index < len(self.data_frame_anormal):
            row = self.data_frame_anormal.iloc[self.anormal_row_index]
            self.adate_time_box.config(text=row['DateTime'])
            self.areal_value_box.config(text=row['Toronto'])
            self.apredict_value_box.config(text=row['Predicted'])
            self.adiffer_box.config(text=row['Abs_Val_Err'])
            self.anormal_row_index += 1

    def open_welcome_page(self):
        from first_window import FirstWindow
        self.root.destroy()
        FirstWindow()

    def open_graphic_representation(self):
        from fourth_window import FourthWindow
        self.root.destroy()
        FourthWindow()

if __name__ == "__main__":
    SecondWindow()
