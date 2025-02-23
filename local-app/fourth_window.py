import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter

class FourthWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="light blue")
        self.root.title("Capstone Project BV03_w3")
        # Title Label
        tk.Label(self.root, text="Graphic Representation I", font=("Times New Roman", 30, "bold"), bg="light blue", fg="black").pack(pady=1)
        # Back Button
        tk.Button(self.root, text="Back to Window 2", font=("Times New Roman", 22, "bold"), bg="green", fg="black", command=self.open_second_window).place(x=200, y=1010)
        # Graphic Representation II Button
        tk.Button(self.root, text="Graphic Representation II", font=("Times New Roman", 22, "bold"), bg="orange", fg="black", command=self.open_graphic_representation_ii).place(x=1400, y=1010)
        # Run Graph Button
        tk.Button(self.root, text="Run Graph I", font=("Times New Roman", 22, "bold"), bg="blue", fg="white", command=self.run_graph).place(x=850, y=1010)
        # Rectangular Box
        self.box = tk.Frame(self.root, bg="white", width=self.root.winfo_screenwidth(), height=945)
        self.box.place(x=0, y=55)
        # Label Inside the Box
        tk.Label(self.box, text="Graph for all data", font=("Times New Roman", 10, "bold"), bg="white", fg="black").place(x=2, y=1)
        self.root.mainloop()
        # Open Previous Window
    def open_second_window(self):
        from second_window import SecondWindow
        self.root.destroy()
        SecondWindow()
        # Open the Next Window
    def open_graphic_representation_ii(self):
        from fifth_window import FifthWindow
        self.root.destroy()
        FifthWindow()
        # Script to Display the Graph
    def run_graph(self):
        file_path = r"C:\Users\OWNER\Desktop\Year 6\Winter 2024\ELE 70B\Presentation2\TrainedData_1.csv"
        data = pd.read_csv(file_path)
        # Prepare data
        data['DateTime'] = pd.to_datetime(data['DateTime'])
        dates = data['DateTime']
        toronto_values = data['Toronto']
        predicted_values = data['Predicted']
        abs_val_err = data['Abs_Val_Err']
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 9))
        # First graph: Real Values vs Prediction
        ax1.plot(dates, toronto_values, label='Toronto', color='blue', linewidth=2)
        ax1.plot(dates, predicted_values, label='Predicted', color='orange', linewidth=2)
        ax1.set_title('Real Values vs Prediction', fontsize=14)
        ax1.set_ylabel('Values')
        ax1.legend()
        ax1.grid(True)
        # Second graph: Error of Real Values vs Prediction
        ax2.plot(dates, abs_val_err, label='Abs_Val_Err', color='green', linewidth=2)
        ax2.axhline(y=1000, color='red', linewidth=3, linestyle='--', label='Anomaly Detection')
        ax2.set_title('Error of Real Values vs Prediction', fontsize=14)
        ax2.set_ylabel('Error')
        ax2.legend()
        ax2.grid(True)
        # Format x-axis for both graphs
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_locator(MonthLocator(interval=6))
            ax.xaxis.set_major_formatter(DateFormatter('%b %Y'))
            ax.tick_params(axis='x', rotation=45)
            ax.set_xlabel('DateTime')
        plt.tight_layout()
        # Embed the plot into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.box)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(relx=0.5, rely=0.5, anchor="center")
        canvas.draw()
