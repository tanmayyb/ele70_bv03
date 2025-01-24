## ELE70A/B Capstone - Forecast Energy Demand with Weather!
 

 ## Requirements
 1. (Optional) Install Python 3.9 or later. (Recommended) Uninstall any previous versions of Python and install [Python 3.12](https://www.python.org/downloads/release/python-3128/)
 2. (Optional) With command prompt/termonal/powershell, run `python --version` to check if Python is installed.
 3. Download Git for Windows from https://git-scm.com/download/win
 4. Run the downloaded installer (Git-X.XX.X-64-bit.exe)
 5. Accept the default settings during installation
 6. Open Command Prompt and verify Git is installed by running:
      ```
      git --version
      ```

## Setup
With terminal (command prompt/powershell) open at a directory of your choice, run the following command:
    ```
    git clone https://github.com/tanmayyb/tmu-capstone-anomaly-detection.git && cd ELE70A-Capstone-2025 && setup.bat && call env.bat && pip install -r requirements.txt
    ```
Or you can run the commands individually:
1. clone the repository:
    ```
    git clone https://github.com/tanmayyb/tmu-capstone-anomaly-detection.git
    ```
2. navigate to the repository:
    ```
    cd ELE70A-Capstone-2025
    ```
 3. Run `setup.bat`:
    ```
    setup.bat
    ```
 4. Run `env.bat`:
    ```
    call env.bat
    ```
    Use this to activate the virtual environment each time you open a new terminal. Use `deactivate` to exit the virtual environment.
 5. Run `pip install -r requirements.txt`:
    ```
    pip install -r requirements.txt
    ```

