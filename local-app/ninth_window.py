import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import MonthLocator, DateFormatter

class NinthWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="light blue")
        self.root.title("Capstone Project BV03_w8")

        # Title Label
        tk.Label(self.root, text="Graphic Representation VI", font=("Times New Roman", 30, "bold"), bg="light blue", fg="black").pack(pady=5)

        # Rectangular Box
        self.box = tk.Frame(self.root, bg="white", width=self.root.winfo_screenwidth(), height=945)
        self.box.place(x=0, y=55)

        # Label Inside the Box
        tk.Label(self.box, text="Graph for Worse Data Prediction", font=("Times New Roman", 10, "bold"), bg="white", fg="black").place(x=2, y=1)

        # Buttons
        tk.Button(self.root, text="Back to Graph V", font=("Times New Roman", 22, "bold"), bg="green", fg="black", command=self.back_to_graph_v).place(x=200, y=1010)
        tk.Button(self.root, text="Graphic Representation VII", font=("Times New Roman", 22, "bold"), bg="orange", fg="black", command=self.open_graphic_representation_vii).place(x=1400, y=1010)
        tk.Button(self.root, text="Run Graph VI", font=("Times New Roman", 22, "bold"), bg="blue", fg="white", command=self.run_graph_vi).place(x=850, y=1010)

        # Load Data
        self.file_path = r"C:\Users\OWNER\Desktop\Year 6\Winter 2024\ELE 70B\Presentation2\AnormalToPrediction_1.csv"
        self.data = pd.read_csv(self.file_path)
        self.data['DateTime'] = pd.to_datetime(self.data['DateTime'])  # Keep DateTime format as is

        # Initialize Figure and Axes for Graph
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(18, 9), constrained_layout=True)

        self.root.mainloop()

    def back_to_graph_v(self):
        from eighth_window import EighthWindow
        self.root.destroy()
        EighthWindow()

    def open_graphic_representation_vii(self):
        from tenth_window import TenthWindow  # Placeholder for the next window
        self.root.destroy()
        TenthWindow()

    def run_graph_vi(self):
        """Displays the graph inside the rectangular box."""
        self.plot_graphs()
        canvas = FigureCanvasTkAgg(self.figure, master=self.box)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(relx=0.5, rely=0.5, anchor="center")
        canvas.draw()

    def plot_graphs(self):
        """Plots Real Values vs Prediction and Error of Real Values vs Prediction."""
        dates = self.data['DateTime']
        toronto_values = self.data['Toronto']
        predicted_values = self.data['Predicted']
        abs_val_err = self.data['Abs_Val_Err']

        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()

        # Plot Graph 1: Real Values vs Prediction
        self.ax1.plot(dates, toronto_values, label='Toronto', color='blue', linewidth=2)
        self.ax1.plot(dates, predicted_values, label='Predicted', color='orange', linewidth=2)
        self.ax1.set_title('Real Values vs Prediction', fontsize=14)
        self.ax1.set_ylabel('Values')
        self.ax1.legend()
        self.ax1.grid(True)

        # Plot Graph 2: Error of Real Values vs Prediction
        self.ax2.plot(dates, abs_val_err, label='Abs_Val_Err', color='green', linewidth=2)
        self.ax2.axhline(y=1000, color='red', linewidth=3, linestyle='--', label='Anomaly Detection')
        self.ax2.set_title('Error of Real Values vs Prediction', fontsize=14)
        self.ax2.set_ylabel('Error')
        self.ax2.legend()
        self.ax2.grid(True)

        # Format x-axis
        for ax in [self.ax1, self.ax2]:
            ax.xaxis.set_major_locator(MonthLocator(interval=6))
            ax.xaxis.set_major_formatter(DateFormatter('%b %Y'))
            ax.tick_params(axis='x', rotation=45)
            ax.set_xlabel('DateTime')

        self.figure.canvas.draw()
