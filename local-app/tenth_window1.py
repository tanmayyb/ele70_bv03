import tkinter as tk

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

        self.root.mainloop()

    def back_to_graph_vi(self):
        from ninth_window import NinthWindow
        self.root.destroy()
        NinthWindow()

    def end_presentation(self):
        """Closes the tenth window and ends the presentation."""
        self.root.destroy()

    def run_graph_vii(self):
        """Placeholder function for running Graph VII."""
        print("Run Graph VII function triggered.")

    def next_days(self):
        """Placeholder function for Next Days functionality."""
        print("Next Days function triggered.")

    def previous_days(self):
        """Placeholder function for Previous Days functionality."""
        print("Previous Days function triggered.")
