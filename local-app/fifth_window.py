import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class FifthWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="light blue")
        self.root.title("Capstone Project BV03_w4")
        # Title Label
        tk.Label(self.root, text="Graphic Representation II", font=("Times New Roman", 30, "bold"), bg="light blue", fg="black").pack(pady=5)
        # Rectangular Box
        self.box = tk.Frame(self.root, bg="white", width=self.root.winfo_screenwidth(), height=945)
        self.box.place(x=0, y=55)
        # Label Inside the Box
        tk.Label(self.box, text="Graph for all data", font=("Times New Roman", 10, "bold"), bg="white", fg="black").place(x=2, y=1)
        # Back to Graph I Button
        tk.Button(self.root, text="Back to Graph I", font=("Times New Roman", 22, "bold"), bg="green", fg="black", command=self.open_graphic_representation_i).place(x=200, y=1010)
        # Graphic Representation III Button
        tk.Button(self.root, text="Graphic Representation III", font=("Times New Roman", 22, "bold"), bg="orange", fg="black", command=self.open_graphic_representation_iii).place(x=1400, y=1010)
        # Run Graph II Button
        tk.Button(self.root, text="Run Graph II", font=("Times New Roman", 22, "bold"), bg="blue", fg="white", command=self.run_graph_ii).place(x=850, y=1010)
        self.root.mainloop()

    def open_graphic_representation_i(self):
        from fourth_window import FourthWindow
        self.root.destroy()
        FourthWindow()

    def open_graphic_representation_iii(self):
        from sixth_window import SixthWindow
        self.root.destroy()
        SixthWindow()

    def run_graph_ii(self):
        file_path = r"C:\Users\OWNER\Desktop\Year 6\Winter 2024\ELE 70B\Presentation2\TrainedData_1.csv"
        data = pd.read_csv(file_path)
        data['DateTime'] = pd.to_datetime(data['DateTime'])
        fig, axs = plt.subplots(2, 1, figsize=(18, 9), constrained_layout=True)
        axs[0].plot(data['DateTime'], data['Toronto'], label='Toronto', color='blue', linewidth=2)
        axs[0].plot(data['DateTime'], data['Predicted'], label='Predicted', color='orange', linewidth=2)
        error_indices = data['Abs_Val_Err'] >= 1000
        axs[0].scatter(data['DateTime'][error_indices], data['Toronto'][error_indices], color='red', label='Error >= 1000', zorder=5)
        axs[0].set_title('Real Values vs Prediction')
        axs[0].set_ylabel('Values')
        axs[0].legend()
        axs[0].grid(True)
        axs[1].plot(data['DateTime'], data['Abs_Val_Err'], label='Abs_Val_Err', color='green', linewidth=2)
        axs[1].axhline(y=1000, color='red', linewidth=2, linestyle='--', label='Anomaly Detection')
        axs[1].set_title('Error of Real Values vs Prediction')
        axs[1].set_ylabel('Error')
        axs[1].legend()
        axs[1].grid(True)
        for ax in axs:
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
            ax.tick_params(axis='x', rotation=45)
        canvas = FigureCanvasTkAgg(fig, master=self.box)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(relx=0.5, rely=0.5, anchor="center")
        canvas.draw()
