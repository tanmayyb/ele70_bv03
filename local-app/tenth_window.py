import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TenthWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="light blue")
        self.root.title("Capstone Project BV03_w9")

        # Title Label
        tk.Label(self.root, text="Graphic Representation VII", font=("Times New Roman", 30, "bold"), bg="light blue", fg="black").pack(pady=5)

        # Rectangular Box
        self.box = tk.Frame(self.root, bg="white", width=self.root.winfo_screenwidth(), height=945)
        self.box.place(x=0, y=55)

        # Label Inside the Box
        tk.Label(self.box, text="Graph for Worse Data Prediction", font=("Times New Roman", 10, "bold"), bg="white", fg="black").place(x=2, y=1)

        # Buttons
        tk.Button(self.root, text="Back to Graph VI", font=("Times New Roman", 22, "bold"), bg="green", fg="black", command=self.back_to_graph_vi).place(x=200, y=1010)
        tk.Button(self.root, text="End Presentation", font=("Times New Roman", 22, "bold"), bg="orange", fg="black", command=self.end_presentation).place(x=1400, y=1010)
        tk.Button(self.root, text="Run Graph VII", font=("Times New Roman", 22, "bold"), bg="blue", fg="white", command=self.run_graph_vii).place(x=850, y=1010)
        tk.Button(self.root, text="Next Days", font=("Times New Roman", 22, "bold"), bg="green", fg="black", command=self.next_days).place(x=1100, y=1010)
        tk.Button(self.root, text="Previous Days", font=("Times New Roman", 22, "bold"), bg="green", fg="black", command=self.previous_days).place(x=600, y=1010)

        # Load Data
        self.file_path = r"C:\\Users\\OWNER\\Desktop\\Year 6\\Winter 2024\\ELE 70B\\Presentation2\\AnormalToPrediction_1.csv"
        self.data = pd.read_csv(self.file_path)
        self.data['DateTime'] = self.data['DateTime']  # Keep DateTime format as is

        # Initialize graph parameters
        self.rows_per_graph = 48
        self.current_start_index = 0
        self.figure, self.axs = plt.subplots(2, 1, figsize=(18, 9), constrained_layout=True)

        self.root.mainloop()

    def back_to_graph_vi(self):
        from ninth_window import NinthWindow
        self.root.destroy()
        NinthWindow()

    def end_presentation(self):
        self.root.destroy()

    def run_graph_vii(self):
        self.plot_graphs(self.current_start_index)
        canvas = FigureCanvasTkAgg(self.figure, master=self.box)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(relx=0.5, rely=0.5, anchor="center")
        canvas.draw()

    def plot_graphs(self, start_index):
        end_index = start_index + self.rows_per_graph
        subset = self.data[start_index:end_index]
        
        if subset.empty:
            print("No more data to display.")
            return

        x_data = subset['DateTime']
        y_toronto = subset['Toronto']
        y_predicted = subset['Predicted']
        y_abs_err = subset['Abs_Val_Err']

        self.axs[0].clear()
        self.axs[1].clear()

        self.axs[0].plot(x_data, y_toronto, label='Toronto', color='blue', linewidth=2)
        self.axs[0].plot(x_data, y_predicted, label='Predicted', color='orange', linewidth=2)
        error_mask = y_abs_err >= 1000
        self.axs[0].plot(x_data[error_mask], y_toronto[error_mask], 'ro', label='Error >= 1000')
        self.axs[0].set_title("Real Values vs Prediction")
        self.axs[0].set_xlabel("DateTime")
        self.axs[0].set_ylabel("Values")
        self.axs[0].legend()
        self.axs[0].grid(True)
        self.axs[0].tick_params(axis='x', rotation=45)

        self.axs[1].plot(x_data, y_abs_err, label='Abs_Val_Err', color='green', linewidth=2)
        self.axs[1].axhline(y=1000, color='red', linewidth=3, linestyle='--', label='Anomaly Detection')
        self.axs[1].set_title("Error of Real Values vs Prediction")
        self.axs[1].set_xlabel("DateTime")
        self.axs[1].set_ylabel("Absolute Error")
        self.axs[1].legend()
        self.axs[1].grid(True)
        self.axs[1].tick_params(axis='x', rotation=45)

        self.figure.canvas.draw()

    def next_days(self):
        self.current_start_index += self.rows_per_graph
        self.plot_graphs(self.current_start_index)

    def previous_days(self):
        self.current_start_index = max(0, self.current_start_index - self.rows_per_graph)
        self.plot_graphs(self.current_start_index)
