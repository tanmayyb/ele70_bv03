import tkinter as tk

class ThirdWindow:
    @staticmethod
    def add_project_directory_box(window):
        var_csv = tk.StringVar(value="")
        frame = tk.Frame(window, bg="white", width=650, height=300, highlightbackground="black", highlightthickness=3)
        frame.place(relx=0.3, rely=0.2, anchor="ne")
        tk.Label(frame, text="       Project Directory       ", font=("Times New Roman", 30, "bold"), bg="white", fg="black").pack(pady=(10, 20))

        tk.Radiobutton(frame, text="CSV file 1", font=("Times New Roman", 20), bg="white", variable=var_csv, value="CSV file 1").pack(anchor="w", padx=10, pady=(0, 10))
        tk.Radiobutton(frame, text="CSV file 2", font=("Times New Roman", 20), bg="white", variable=var_csv, value="CSV file 2").pack(anchor="w", padx=10)

        return var_csv

    @staticmethod
    def add_modules_box(window):
        var_model = tk.StringVar(value="")
        frame = tk.Frame(window, bg="light green", width=400, height=300, highlightbackground="black", highlightthickness=3)
        frame.place(relx=0.3, rely=0.4, anchor="ne")
        tk.Label(frame, text="Modules", font=("Times New Roman", 30, "bold"), bg="light green", fg="black").pack(pady=(10, 20))

        tk.Radiobutton(frame, text="XGBoost Model:eXtr Grad Boost", font=("Times New Roman", 20), bg="light green", variable=var_model, value="XGBoost Model:eXtr Grad Boost").pack(anchor="w", padx=10, pady=(0, 10))
        tk.Radiobutton(frame, text="ARIMA Model:Auto Int Mov Aver", font=("Times New Roman", 20), bg="light green", variable=var_model, value="ARIMA Model:Auto Int Mov Aver").pack(anchor="w", padx=10)

        return var_model

    @staticmethod
    def add_progress_box(window):
        return ThirdWindow.create_box(window, 250, 800, "        Progress        ", "0.00 %")

    @staticmethod
    def create_box(window, x, y, text, subtext, width=275, height=125):
        box = tk.Frame(window, bg="white", width=width, height=height, highlightbackground="black", highlightthickness=3)
        box.place(x=x, y=y)
        tk.Label(box, text=text, font=("Times New Roman", 20, "bold"), bg="white", fg="black").pack(anchor="n")
        label = tk.Label(box, text=subtext, font=("Times New Roman", 16), bg="white", fg="black")
        label.pack(anchor="s")
        return label

    @staticmethod
    def add_date_time_box(window): return ThirdWindow.create_box(window, 1350, 340, "     Date & Time     ", "----/--/-- ; 00:00")

    @staticmethod
    def add_real_value_box(window): return ThirdWindow.create_box(window, 1075, 435, "     Real_Val     ", "0.00")

    @staticmethod
    def add_predict_value_box(window): return ThirdWindow.create_box(window, 1370, 435, "     Pred_Val     ", "0.00")

    @staticmethod
    def add_differ_box(window): return ThirdWindow.create_box(window, 1670, 435, "     Difference     ", "0.00")

    @staticmethod
    def add_adate_time_box(window): return ThirdWindow.create_box(window, 1355, 700, "    A_Date & Time    ", "----/--/-- ; 00:00")

    @staticmethod
    def add_areal_value_box(window): return ThirdWindow.create_box(window, 1070, 795, "    A_Real_Val    ", "0.00")

    @staticmethod
    def add_apredict_value_box(window): return ThirdWindow.create_box(window, 1375, 795, "    A_Pred_Val    ", "0.00")

    @staticmethod
    def add_adiffer_box(window): return ThirdWindow.create_box(window, 1665, 795, "    A_Difference    ", "0.00")
