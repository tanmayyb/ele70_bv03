import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import MonthLocator, DateFormatter

class SeventhWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="light blue")
        self.root.title("Capstone Project BV03_w6")
        tk.Label(self.root, text="Graphic Representation IV", font=("Times New Roman", 30, "bold"), bg="light blue", fg="black").pack(pady=5)
        self.box = tk.Frame(self.root, bg="white", width=self.root.winfo_screenwidth(), height=945)
        self.box.place(x=0, y=55)
        tk.Label(self.box, text="Graph for Best Data Prediction", font=("Times New Roman", 10, "bold"), bg="white", fg="black").place(x=2, y=1)
        tk.Button(self.root, text="Back to Graph III", font=("Times New Roman", 22, "bold"), bg="green", fg="black", command=self.back_to_graph_iii).place(x=200, y=1010)
        tk.Button(self.root, text="Graphic Representation V", font=("Times New Roman", 22, "bold"), bg="orange", fg="black", command=self.open_graphic_representation_v).place(x=1400, y=1010)
        tk.Button(self.root, text="Run Graph IV", font=("Times New Roman", 22, "bold"), bg="blue", fg="white", command=self.run_graph_iv).place(x=850, y=1010)
        self.root.mainloop()

    def back_to_graph_iii(self):
        from sixth_window import SixthWindow
        self.root.destroy()
        SixthWindow()

    def open_graphic_representation_v(self):
        from eighth_window import EighthWindow
        self.root.destroy()
        EighthWindow()

    def run_graph_iv(self):
        file_path = r"C:\Users\OWNER\Desktop\Year 6\Winter 2024\ELE 70B\Presentation2\NormalToPrediction_1.csv"
        data = pd.read_csv(file_path)
        data['DateTime'] = pd.to_datetime(data['DateTime'])
        dates = data['DateTime']
        toronto_values = data['Toronto']
        predicted_values = data['Predicted']
        abs_val_err = data['Abs_Val_Err']
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 9), constrained_layout=True)
        ax1.plot(dates, toronto_values, label='Toronto', color='blue', linewidth=2)
        ax1.plot(dates, predicted_values, label='Predicted', color='orange', linewidth=2)
        ax1.set_title('Real Values vs Prediction', fontsize=14)
        ax1.set_ylabel('Values')
        ax1.legend()
        ax1.grid(True)
        ax2.plot(dates, abs_val_err, label='Abs_Val_Err', color='green', linewidth=2)
        ax2.axhline(y=1000, color='red', linewidth=3, linestyle='--', label='Anomaly Detection')
        ax2.set_title('Error of Real Values vs Prediction', fontsize=14)
        ax2.set_ylabel('Error')
        ax2.legend()
        ax2.grid(True)
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_locator(MonthLocator(interval=6))
            ax.xaxis.set_major_formatter(DateFormatter('%b %Y'))
            ax.tick_params(axis='x', rotation=45)
            ax.set_xlabel('DateTime')
        canvas = FigureCanvasTkAgg(fig, master=self.box)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(relx=0.5, rely=0.5, anchor="center")
        canvas.draw()
