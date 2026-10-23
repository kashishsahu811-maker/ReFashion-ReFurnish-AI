@echo off
title ReFashion ^& ReFurnish AI
echo ========================================================
echo        Starting ReFashion ^& ReFurnish AI
echo ========================================================
echo.
echo Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    pause
    exit /b
)

echo.
echo Installing/verifying dependencies...
pip install -r requirements.txt

echo.
echo Launching Streamlit web application...
echo App will open in your default browser at http://localhost:8501
echo Press Ctrl+C in this terminal window to stop the server.
echo.
streamlit run app.py

pause
