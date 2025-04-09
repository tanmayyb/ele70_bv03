import customtkinter as ctk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import urllib.request
api_url = 'https://raw.githubusercontent.com/tanmayyb/ele70_bv03/refs/heads/main/api/datasets.py'
exec(urllib.request.urlopen(api_url).read())


# Global style variables
STYLES = {
    # Fonts
    "title_font": ("Arial", 24, "bold"),
    "header_font": ("Arial", 20, "bold"),
    "subtitle_font": ("Arial", 16, "bold"),
    "text_font": ("Arial", 14),
    "button_font": ("Arial", 14),
    
    # Colors
    "primary_color": "#3498db",
    "secondary_color": "#2ecc71",
    "accent_color": "#e74c3c",
    "bg_color": "#2d2d2d",
    "text_color": "#ffffff",
    
    # Sizes
    "button_height": 40,
    "corner_radius": 8,
    "padding_small": 10,
    "padding_medium": 20,
    "padding_large": 40,
    
    # Specific elements
    "welcome_title_font": ("Arial", 48, "bold"),
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Machine Learning App")
        self.geometry("1200x750")
        ctk.set_appearance_mode("dark")
        
        # Configure grid to make the app resizable
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.frames = {}
        for F in (WelcomePage, DatasetSelectionPage, LoadDatasetPage, CreateDatasetPage, ModelSelectionPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(WelcomePage)
    
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

class WelcomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure grid to make the frame resizable
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        # Create a container frame for better structure
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=STYLES["padding_medium"], pady=STYLES["padding_medium"])
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Title with improved styling
        label = ctk.CTkLabel(content_frame, text="BV03", font=STYLES["welcome_title_font"])
        label.grid(row=0, column=0, sticky="nsew")
        
        # Button container for consistent placement
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, sticky="ew", padx=STYLES["padding_medium"], pady=(0, STYLES["padding_medium"]))
        button_frame.grid_columnconfigure(0, weight=1)
        
        button = ctk.CTkButton(button_frame, text="Next", 
                              font=STYLES["button_font"],
                              height=STYLES["button_height"],
                              corner_radius=STYLES["corner_radius"],
                              command=lambda: parent.show_frame(DatasetSelectionPage))
        button.grid(row=0, column=0, pady=STYLES["padding_small"], padx=100)

class DatasetSelectionPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure grid to make the frame resizable
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create a container frame for better structure
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=STYLES["padding_large"], pady=STYLES["padding_large"])
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(content_frame, text="Dataset Selection", font=STYLES["title_font"])
        title.grid(row=0, column=0, sticky="ew", pady=(0, STYLES["padding_medium"]))
        
        # Buttons with improved styling
        load_btn = ctk.CTkButton(content_frame, text="Load Dataset", 
                                font=STYLES["button_font"],
                                height=STYLES["button_height"],
                                corner_radius=STYLES["corner_radius"],
                                command=lambda: parent.show_frame(LoadDatasetPage))
        load_btn.grid(row=1, column=0, pady=STYLES["padding_small"], padx=100, sticky="ew")
        
        create_btn = ctk.CTkButton(content_frame, text="Create New Dataset", 
                                  font=STYLES["button_font"],
                                  height=STYLES["button_height"],
                                  corner_radius=STYLES["corner_radius"],
                                  command=lambda: parent.show_frame(CreateDatasetPage))
        create_btn.grid(row=2, column=0, pady=STYLES["padding_small"], padx=100, sticky="ew")
        
        home_btn = ctk.CTkButton(content_frame, text="Home", 
                                font=STYLES["button_font"],
                                height=STYLES["button_height"],
                                corner_radius=STYLES["corner_radius"],
                                command=lambda: parent.show_frame(WelcomePage))
        home_btn.grid(row=3, column=0, pady=STYLES["padding_small"], padx=100, sticky="ew")

class LoadDatasetPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure grid to make the frame resizable
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create a container frame for better structure
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=STYLES["padding_large"], pady=STYLES["padding_large"])
        content_frame.grid_columnconfigure(0, weight=1)
        
        self.dataset_path = ctk.StringVar()
        
        # Title
        title = ctk.CTkLabel(content_frame, text="Load Dataset", font=STYLES["title_font"])
        title.grid(row=0, column=0, sticky="ew", pady=(0, STYLES["padding_medium"]))
        
        # File selection section
        file_frame = ctk.CTkFrame(content_frame)
        file_frame.grid(row=1, column=0, sticky="ew", pady=STYLES["padding_small"])
        file_frame.grid_columnconfigure(0, weight=1)
        file_frame.grid_columnconfigure(1, weight=0)
        
        entry = ctk.CTkEntry(file_frame, textvariable=self.dataset_path, width=400)
        entry.grid(row=0, column=0, padx=(STYLES["padding_small"], 5), pady=STYLES["padding_small"], sticky="ew")
        
        browse_btn = ctk.CTkButton(file_frame, text="Browse", 
                                  font=STYLES["button_font"],
                                  command=self.load_file)
        browse_btn.grid(row=0, column=1, padx=(5, STYLES["padding_small"]), pady=STYLES["padding_small"])
        
        # Navigation buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", pady=STYLES["padding_medium"])
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
        home_btn = ctk.CTkButton(button_frame, text="Home", 
                                font=STYLES["button_font"],
                                height=STYLES["button_height"],
                                corner_radius=STYLES["corner_radius"],
                                command=lambda: parent.show_frame(WelcomePage))
        home_btn.grid(row=0, column=0, pady=STYLES["padding_small"], padx=STYLES["padding_small"], sticky="ew")
        
        back_btn = ctk.CTkButton(button_frame, text="Back", 
                                font=STYLES["button_font"],
                                height=STYLES["button_height"],
                                corner_radius=STYLES["corner_radius"],
                                command=lambda: parent.show_frame(DatasetSelectionPage))
        back_btn.grid(row=0, column=1, pady=STYLES["padding_small"], padx=STYLES["padding_small"], sticky="ew")
        
        next_btn = ctk.CTkButton(button_frame, text="Next", 
                                font=STYLES["button_font"],
                                height=STYLES["button_height"],
                                corner_radius=STYLES["corner_radius"],
                                command=lambda: parent.show_frame(ModelSelectionPage))
        next_btn.grid(row=0, column=2, pady=STYLES["padding_small"], padx=STYLES["padding_small"], sticky="ew")
    
    def load_file(self):
        file_path = filedialog.askopenfilename()
        self.dataset_path.set(file_path)

class CreateDatasetPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure grid to make the frame resizable
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create a container frame for better structure
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=STYLES["padding_large"], pady=STYLES["padding_large"])
        content_frame.grid_columnconfigure(0, weight=1)
        
        self.energy_options = ["ZONAL", "FSA"]
        dummy_options = ["Option1", "Option2"]
        predictor_options = ["Climate"]
        self.target_options = ["Option"]
        
        # Title
        title = ctk.CTkLabel(content_frame, text="Create Dataset", font=STYLES["title_font"])
        title.grid(row=0, column=0, sticky="ew", pady=(0, STYLES["padding_medium"]))
        
        # Form fields
        form_frame = ctk.CTkFrame(content_frame)
        form_frame.grid(row=1, column=0, sticky="ew", pady=STYLES["padding_small"])
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Energy Repository
        ctk.CTkLabel(form_frame, text="Select Energy Repository:", 
                    font=STYLES["text_font"], 
                    anchor="w").grid(row=0, column=0, sticky="w", padx=STYLES["padding_small"], pady=5)
        energy_combo = ctk.CTkComboBox(form_frame, values=self.energy_options, width=300, 
                                     command=self.on_energy_select)
        energy_combo.grid(row=0, column=1, sticky="ew", padx=STYLES["padding_small"], pady=5)
        
        # Target Zone
        ctk.CTkLabel(form_frame, text="Select Target Zone:", 
                    font=STYLES["text_font"], 
                    anchor="w").grid(row=1, column=0, sticky="w", padx=STYLES["padding_small"], pady=5)
        self.target_combo = ctk.CTkComboBox(form_frame, values=dummy_options, width=300,
                                     command=self.on_target_select)
        self.target_combo.grid(row=1, column=1, sticky="ew", padx=STYLES["padding_small"], pady=5)
        
        # Dataset Range
        ctk.CTkLabel(form_frame, text="Select Dataset Range:", 
                    font=STYLES["text_font"], 
                    anchor="w").grid(row=2, column=0, sticky="w", padx=STYLES["padding_small"], pady=5)
        
        # Create a subframe for the date range dropdowns
        date_range_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_range_frame.grid(row=2, column=1, sticky="ew", padx=STYLES["padding_small"], pady=5)
        date_range_frame.grid_columnconfigure(0, weight=1)
        date_range_frame.grid_columnconfigure(1, weight=0)
        date_range_frame.grid_columnconfigure(2, weight=1)
        
        # Start date dropdown
        ctk.CTkLabel(date_range_frame, text="Start Date:", 
                    font=STYLES["text_font"], 
                    anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.date_options = ["2020-01", "2020-02", "2020-03", "2020-04", "2020-05", "2020-06"]
        self.start_date = ctk.CTkComboBox(date_range_frame, values=self.date_options, width=140)
        self.start_date.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        
        # Separator
        ctk.CTkLabel(date_range_frame, text="to", 
                    font=STYLES["text_font"], 
                    anchor="center").grid(row=1, column=1, padx=5)
        
        # End date dropdown
        ctk.CTkLabel(date_range_frame, text="End Date:", 
                    font=STYLES["text_font"], 
                    anchor="w").grid(row=0, column=2, sticky="w", pady=(0, 5))
        self.end_date = ctk.CTkComboBox(date_range_frame, values=self.date_options, width=140)
        self.end_date.set(self.date_options[-1])  # Set default to last date
        self.end_date.grid(row=1, column=2, sticky="ew", padx=(5, 0))
        
        # Predictor Repository
        ctk.CTkLabel(form_frame, text="Select Predictor Repository:", 
                    font=STYLES["text_font"], 
                    anchor="w").grid(row=3, column=0, sticky="w", padx=STYLES["padding_small"], pady=5)
        ctk.CTkComboBox(form_frame, values=predictor_options, width=300).grid(row=3, column=1, sticky="ew", padx=STYLES["padding_small"], pady=5)
        
        # Navigation buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", pady=STYLES["padding_medium"])
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
        home_btn = ctk.CTkButton(button_frame, text="Home", 
                                font=STYLES["button_font"],
                                height=STYLES["button_height"],
                                corner_radius=STYLES["corner_radius"],
                                command=lambda: parent.show_frame(WelcomePage))
        home_btn.grid(row=0, column=0, pady=STYLES["padding_small"], padx=STYLES["padding_small"], sticky="ew")
        
        back_btn = ctk.CTkButton(button_frame, text="Back", 
                                font=STYLES["button_font"],
                                height=STYLES["button_height"],
                                corner_radius=STYLES["corner_radius"],
                                command=lambda: parent.show_frame(DatasetSelectionPage))
        back_btn.grid(row=0, column=1, pady=STYLES["padding_small"], padx=STYLES["padding_small"], sticky="ew")
        
        next_btn = ctk.CTkButton(button_frame, text="Next", 
                                font=STYLES["button_font"],
                                height=STYLES["button_height"],
                                corner_radius=STYLES["corner_radius"],
                                command=lambda: parent.show_frame(ModelSelectionPage))
        next_btn.grid(row=0, column=2, pady=STYLES["padding_small"], padx=STYLES["padding_small"], sticky="ew")

    def on_energy_select(self, choice):
        print(f"Selected energy repository: {choice}")
        self.ieso = IESODataset(choice) 

        target_options = self.ieso.get_target_options() # returns list of the target options
        available_dates = self.ieso.get_dates() # returns list of available dates (str)
        available_dates = [str(date) for date in available_dates]
        self.target_combo.configure(values=target_options)
        self.start_date.configure(values=available_dates)
        self.end_date.configure(values=available_dates)
        
    def on_target_select(self, choice):
        print(f"Selected target zone: {choice}")
        self.ieso.set_target(choice)
        # Add your callback logic here

class ModelSelectionPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure grid to make the frame resizable
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create a container frame for better structure
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=STYLES["padding_large"], pady=STYLES["padding_large"])
        content_frame.grid_columnconfigure(0, weight=1)
        
        self.model_var = ctk.StringVar(value="Model1")
        
        # Title
        title = ctk.CTkLabel(content_frame, text="Model Selection", font=STYLES["title_font"])
        title.grid(row=0, column=0, sticky="ew", pady=(0, STYLES["padding_medium"]))
        
        # Model selection options
        model_frame = ctk.CTkFrame(content_frame)
        model_frame.grid(row=1, column=0, sticky="ew", pady=STYLES["padding_small"])
        model_frame.grid_columnconfigure(0, weight=1)
        
        model_label = ctk.CTkLabel(model_frame, text="Select Model:", font=STYLES["subtitle_font"])
        model_label.grid(row=0, column=0, sticky="w", padx=STYLES["padding_medium"], pady=STYLES["padding_small"])
        
        radio_frame = ctk.CTkFrame(model_frame, fg_color="transparent")
        radio_frame.grid(row=1, column=0, sticky="ew", padx=STYLES["padding_large"])
        
        xgboost_radio = ctk.CTkRadioButton(radio_frame, text="XGBoost", 
                                          variable=self.model_var, 
                                          value="Model1",
                                          font=STYLES["text_font"])
        xgboost_radio.grid(row=0, column=0, pady=STYLES["padding_small"], sticky="w")
        
        lstm_radio = ctk.CTkRadioButton(radio_frame, text="LSTM", 
                                       variable=self.model_var, 
                                       value="Model2",
                                       font=STYLES["text_font"])
        lstm_radio.grid(row=1, column=0, pady=STYLES["padding_small"], sticky="w")
        
        # Navigation buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", pady=STYLES["padding_medium"])
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
        home_btn = ctk.CTkButton(button_frame, text="Home", 
                                font=STYLES["button_font"],
                                height=STYLES["button_height"],
                                corner_radius=STYLES["corner_radius"],
                                command=lambda: parent.show_frame(WelcomePage))
        home_btn.grid(row=0, column=0, pady=STYLES["padding_small"], padx=STYLES["padding_small"], sticky="ew")
        
        back_btn = ctk.CTkButton(button_frame, text="Back", 
                                font=STYLES["button_font"],
                                height=STYLES["button_height"],
                                corner_radius=STYLES["corner_radius"],
                                command=lambda: parent.show_frame(LoadDatasetPage))
        back_btn.grid(row=0, column=1, pady=STYLES["padding_small"], padx=STYLES["padding_small"], sticky="ew")
        
        train_btn = ctk.CTkButton(button_frame, text="Train and Analyze", 
                                 font=STYLES["button_font"],
                                 height=STYLES["button_height"],
                                 corner_radius=STYLES["corner_radius"],
                                 fg_color=STYLES["secondary_color"],
                                 command=self.open_dashboard)
        train_btn.grid(row=0, column=2, pady=STYLES["padding_small"], padx=STYLES["padding_small"], sticky="ew")
    
    def open_dashboard(self):
        TrainingDashboard()

class TrainingDashboard(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Training Dashboard")
        self.geometry("1200x750")
        
        # Configure grid to make the window resizable
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Left frame for plots
        frame1 = ctk.CTkFrame(self)
        frame1.grid(row=0, column=0, sticky="nsew", padx=STYLES["padding_small"], pady=STYLES["padding_small"])
        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_rowconfigure(0, weight=0)
        frame1.grid_rowconfigure(1, weight=1)
        
        # Title for plot section
        plot_title = ctk.CTkLabel(frame1, text="Training Progress", font=STYLES["header_font"])
        plot_title.grid(row=0, column=0, sticky="ew", pady=STYLES["padding_small"])
        
        # Plot container
        plot_frame = ctk.CTkFrame(frame1)
        plot_frame.grid(row=1, column=0, sticky="nsew", padx=STYLES["padding_small"], pady=STYLES["padding_small"])
        self.create_plot(plot_frame)
        
        # Right frame for stats
        frame2 = ctk.CTkFrame(self)
        frame2.grid(row=0, column=1, sticky="nsew", padx=STYLES["padding_small"], pady=STYLES["padding_small"])
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_rowconfigure(0, weight=0)
        frame2.grid_rowconfigure(1, weight=1)
        
        # Title for stats section
        stats_title = ctk.CTkLabel(frame2, text="Model Statistics", font=STYLES["header_font"])
        stats_title.grid(row=0, column=0, sticky="ew", pady=STYLES["padding_small"])
        
        # Stats container
        stats_frame = ctk.CTkFrame(frame2)
        stats_frame.grid(row=1, column=0, sticky="nsew", padx=STYLES["padding_small"], pady=STYLES["padding_small"])
        self.create_stats(stats_frame)
    
    def create_plot(self, parent):
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot([1, 2, 3, 4], [1, 4, 9, 16], label="Loss Curve", color=STYLES["primary_color"], linewidth=2)
        ax.set_xlabel("Epochs")
        ax.set_ylabel("Loss")
        ax.set_title("Training and Validation Loss")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Set dark theme for plot
        plt.style.use('dark_background')
        fig.patch.set_facecolor(STYLES["bg_color"])
        ax.set_facecolor(STYLES["bg_color"])
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=STYLES["padding_small"], pady=STYLES["padding_small"])
    
    def create_stats(self, parent):
        stats = {
            "Train Loss": "0.02", 
            "Train Accuracy": "98%", 
            "Test Loss": "0.05", 
            "Test Accuracy": "95%",
            "F1 Score": "0.94",
            "Precision": "0.96",
            "Recall": "0.93"
        }
        
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        row = 0
        for key, value in stats.items():
            label = ctk.CTkLabel(parent, text=key, font=STYLES["text_font"], anchor="e")
            label.grid(row=row, column=0, sticky="e", padx=STYLES["padding_small"], pady=STYLES["padding_small"])
            
            value_label = ctk.CTkLabel(parent, text=value, font=("Arial", 14, "bold"), anchor="w")
            value_label.grid(row=row, column=1, sticky="w", padx=STYLES["padding_small"], pady=STYLES["padding_small"])
            
            row += 1

if __name__ == "__main__":
    app = App()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("Program terminated by user")
        app.destroy()
