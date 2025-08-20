@echo off
echo ========================================
echo  Diabetic Retinopathy Detection App
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Using system Python.
    echo.
)

REM Check if model file exists
if not exist "resnet50_dr_classifier.pth" (
    echo ERROR: Model file 'resnet50_dr_classifier.pth' not found!
    echo Please ensure the model file is in the current directory.
    pause
    exit /b 1
)

echo Starting the application...
echo.
echo The app will open in your web browser at: http://127.0.0.1:7860
echo.
echo Press Ctrl+C to stop the application
echo.

REM Start the application
python app.py

pause
