import tkinter as tk

class FirstWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="light blue")
        self.root.title("Capstone Project BV03_w1")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        # Welcome Label
        tk.Label(self.root, text="WELCOME TO GROUP BV03", font=("Times New Roman", 50, "bold"), bg="light blue", fg="black").pack(pady=(100, 0))
        # Student Label
        tk.Label(self.root, text="          Student Participants          ", font=("Times New Roman", 28, "bold"), bg="yellow", fg="black").pack(pady=(50, 0))
        tk.Label(self.root, bg="white", width=150, height=6, font=("Times New Roman", 20), text=(
            "Student A: Carlos Samuel Mefenya\n"
            "Student B: Tanmay Bishnoi\n"
            "Student C: Prateek Arora\n"
            "Student D: Aranan Thevendran\n"
            "Student E: Farhan Ahmed"
        )).pack(pady=(30, 0))
        # Supervisor Label
        tk.Label(self.root, text="          Faculty Supervisors          ", font=("Times New Roman", 28, "bold"), bg="yellow", fg="black").pack(pady=(50, 0))
        tk.Label(self.root, bg="white", width=150, height=4, font=("Times New Roman", 20), text=(
            "Bala Venkatesh\nShima Bagher Zade Homayie\nAmir Reza Nikzad Ghadikolaei"
        )).pack(pady=(30, 0))
        # Login Button
        tk.Button(self.root, text="Login", font=("Times New Roman", 28, "bold"), bg="green", fg="black", width=8, height=2, command=self.open_second_window).pack(pady=(100, 0))
        # Open Next Window
    def open_second_window(self):
        from second_window import SecondWindow
        self.root.destroy()
        SecondWindow()

if __name__ == "__main__":
    FirstWindow()
