## ELE70A/B Capstone - Forecast Energy Demand with Weather!
 

## Requirements
1. Conda:
   1. Install Conda ([exe](https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Windows-x86_64.exe)) (select all options)

2. Git:
   1. Download Git for Windows from (https://git-scm.com/download/win)
   2. Run the downloaded installer (Git-X.XX.X-64-bit.exe)
   3. Accept the default settings during installation
   4. Open Command Prompt and verify Git is installed by running:
      ```
      git --version
      ```

## Setup
With terminal (command prompt/powershell) open at a directory of your choice, run the following commands:
1. clone the repository:
    ```
    git clone https://github.com/tanmayyb/ele70_bv03.git
    ```
2. navigate to the repository:
    ```
    cd ele70_bv03
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

