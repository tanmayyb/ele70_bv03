import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EighthWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="light blue")
        self.root.title("Capstone Project BV03_w7")

        # Title Label
        tk.Label(self.root, text="Graphic Representation V", font=("Times New Roman", 30, "bold"), bg="light blue", fg="black").pack(pady=5)

        # Rectangular Box
        self.box = tk.Frame(self.root, bg="white", width=self.root.winfo_screenwidth(), height=945)
        self.box.place(x=0, y=55)

        # Label Inside the Box
        tk.Label(self.box, text="Graph for Best Data Prediction", font=("Times New Roman", 10, "bold"), bg="white", fg="black").place(x=2, y=1)

        # Buttons
        tk.Button(self.root, text="Back to Graph IV", font=("Times New Roman", 22, "bold"), bg="green", fg="black", command=self.back_to_graph_iv).place(x=200, y=1010)
        tk.Button(self.root, text="Graphic Representation VI", font=("Times New Roman", 22, "bold"), bg="orange", fg="black", command=self.open_graphic_representation_vi).place(x=1400, y=1010)
        tk.Button(self.root, text="Run Graph V", font=("Times New Roman", 22, "bold"), bg="blue", fg="white", command=self.run_graph_v).place(x=850, y=1010)
        tk.Button(self.root, text="Next Days", font=("Times New Roman", 22, "bold"), bg="green", fg="black", command=self.next_days).place(x=1100, y=1010)
        tk.Button(self.root, text="Previous Days", font=("Times New Roman", 22, "bold"), bg="green", fg="black", command=self.previous_days).place(x=600, y=1010)

        # Load Data
        self.file_path = r"C:\Users\OWNER\Desktop\Year 6\Winter 2024\ELE 70B\Presentation2\NormalToPrediction_1.csv"
        self.data = pd.read_csv(self.file_path)
        self.data['DateTime'] = self.data['DateTime']  # Keep DateTime format as is

        # Graph Settings
        self.rows_per_graph = 48
        self.current_start_index = 0
        self.figure, self.axs = plt.subplots(2, 1, figsize=(18, 9), constrained_layout=True)

        self.root.mainloop()

    def back_to_graph_iv(self):
        from seventh_window import SeventhWindow
        self.root.destroy()
        SeventhWindow()

    def open_graphic_representation_vi(self):
        from ninth_window import NinthWindow  # Placeholder for the next window
        self.root.destroy()
        NinthWindow()

    def run_graph_v(self):
        """Displays the graph inside the rectangular box."""
        self.plot_graphs(self.current_start_index)
        canvas = FigureCanvasTkAgg(self.figure, master=self.box)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(relx=0.5, rely=0.5, anchor="center")
        canvas.draw()

    def next_days(self):
        """Displays the graph for the next 48 rows."""
        if self.current_start_index + self.rows_per_graph < len(self.data):
            self.current_start_index += self.rows_per_graph
            self.plot_graphs(self.current_start_index)

    def previous_days(self):
        """Displays the graph for the previous 48 rows."""
        if self.current_start_index - self.rows_per_graph >= 0:
            self.current_start_index -= self.rows_per_graph
            self.plot_graphs(self.current_start_index)

    def plot_graphs(self, start_index):
        """Plots graphs for a given index range inside the rectangular box."""
        end_index = start_index + self.rows_per_graph
        subset = self.data[start_index:end_index]

        if subset.empty:
            print("No more data to display.")
            return

        # Extract data
        x_data = subset['DateTime']
        y_toronto = subset['Toronto']
        y_predicted = subset['Predicted']
        y_abs_err = subset['Abs_Val_Err']

        # Clear previous plots
        self.axs[0].clear()
        self.axs[1].clear()

        # Plot Graph 1: Real Values vs Prediction
        self.axs[0].plot(x_data, y_toronto, label='Toronto', color='blue', linewidth=2)
        self.axs[0].plot(x_data, y_predicted, label='Predicted', color='orange', linewidth=2)
        error_mask = y_abs_err >= 1000
        self.axs[0].plot(x_data[error_mask], y_toronto[error_mask], 'ro', label='Error >= 1000')  # Highlight errors
        self.axs[0].set_title("Real Values vs Prediction")
        self.axs[0].set_xlabel("DateTime")
        self.axs[0].set_ylabel("Values")
        self.axs[0].legend()
        self.axs[0].grid(True)
        self.axs[0].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for readability

        # Plot Graph 2: Error of Real Values vs Prediction
        self.axs[1].plot(x_data, y_abs_err, label='Abs_Val_Err', color='green', linewidth=2)
        self.axs[1].axhline(y=1000, color='red', linewidth=3, linestyle='--', label='Anomaly Detection')
        self.axs[1].set_title("Error of Real Values vs Prediction")
        self.axs[1].set_xlabel("DateTime")
        self.axs[1].set_ylabel("Absolute Error")
        self.axs[1].legend()
        self.axs[1].grid(True)
        self.axs[1].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for readability

        self.figure.canvas.draw()
