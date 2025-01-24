@echo off
:: Check for default Windows Python installation first
for /f "delims=" %%i in ('where python 2^>nul') do set PYTHON_PATH=%%i


:: Check for Python in standard Windows locations
if "%PYTHON_PATH%"=="" (
    if exist "C:\Python313\python.exe" (
        set "PYTHON_PATH=C:\Python313\python.exe"
    ) else if exist "C:\Python312\python.exe" (
        set "PYTHON_PATH=C:\Python312\python.exe"
    ) else if exist "C:\Python311\python.exe" (
        set "PYTHON_PATH=C:\Python311\python.exe"
    ) else if exist "C:\Python310\python.exe" (
        set "PYTHON_PATH=C:\Python310\python.exe"
    ) else if exist "C:\Python39\python.exe" (
        set "PYTHON_PATH=C:\Python39\python.exe"
    ) else if exist "C:\Program Files\Python313\python.exe" (
        set "PYTHON_PATH=C:\Program Files\Python313\python.exe"
    ) else if exist "C:\Program Files\Python312\python.exe" (
        set "PYTHON_PATH=C:\Program Files\Python312\python.exe"
    ) else if exist "C:\Program Files\Python311\python.exe" (
        set "PYTHON_PATH=C:\Program Files\Python311\python.exe"
    ) else if exist "C:\Program Files\Python310\python.exe" (
        set "PYTHON_PATH=C:\Program Files\Python310\python.exe"
    ) else if exist "C:\Program Files\Python39\python.exe" (
        set "PYTHON_PATH=C:\Program Files\Python39\python.exe"
    ) else if exist "C:\Program Files (x86)\Python313\python.exe" (
        set "PYTHON_PATH=C:\Program Files (x86)\Python313\python.exe"
    ) else if exist "C:\Program Files (x86)\Python312\python.exe" (
        set "PYTHON_PATH=C:\Program Files (x86)\Python312\python.exe"
    ) else if exist "C:\Program Files (x86)\Python311\python.exe" (
        set "PYTHON_PATH=C:\Program Files (x86)\Python311\python.exe"
    ) else if exist "C:\Program Files (x86)\Python310\python.exe" (
        set "PYTHON_PATH=C:\Program Files (x86)\Python310\python.exe"
    ) else if exist "C:\Program Files (x86)\Python39\python.exe" (
        set "PYTHON_PATH=C:\Program Files (x86)\Python39\python.exe"
    )
)

:: If Python not found in standard locations, check Windows Store Python
if "%PYTHON_PATH%"=="" (
    if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
        set "PYTHON_PATH=%LocalAppData%\Programs\Python\Python313\python.exe"
    ) else if exist "%LocalAppData%\Programs\Python\Python312\python.exe" (
        set "PYTHON_PATH=%LocalAppData%\Programs\Python\Python312\python.exe"
    ) else if exist "%LocalAppData%\Programs\Python\Python311\python.exe" (
        set "PYTHON_PATH=%LocalAppData%\Programs\Python\Python311\python.exe"
    ) else if exist "%LocalAppData%\Programs\Python\Python310\python.exe" (
        set "PYTHON_PATH=%LocalAppData%\Programs\Python\Python310\python.exe"
    ) else if exist "%LocalAppData%\Programs\Python\Python39\python.exe" (
        set "PYTHON_PATH=%LocalAppData%\Programs\Python\Python39\python.exe"
    )
)

:: Verify Python was found
if "%PYTHON_PATH%"=="" (
    echo Python installation not found. Please install Python 3.9 or later.
    exit /b 1
)

:: Check if virtualenv is installed
python -m pip show virtualenv >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing virtualenv...
    python -m pip install virtualenv
    if %errorlevel% neq 0 (
        echo Failed to install virtualenv.
        @REM exit /b 1
        echo Try installing virtualenv in case Python/Scripts is not in PATH.
    )
)



:: Create virtual environment
echo Creating virtual environment "bv03"...
python -m virtualenv bv03
if %errorlevel% neq 0 (
    echo Failed to create virtual environment.
    exit /b 1
)



:: Activate the virtual environment
echo Activating the virtual environment...
call bv03\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate the virtual environment.
    exit /b 1
)

:: Confirm activation
echo Virtual environment "bv03" activated. Ready to install packages.
echo Use `deactivate` to exit the virtual environment.
cmd /k
