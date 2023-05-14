@echo off
echo Installing python dependencies...
where pip3 >nul 2>nul
if %errorlevel% neq 0 (
    echo Pip is not installed on this machine. Please install Python and try again.
    pause
    exit /b
)
pip3.exe install openpyxl
pip3.exe install pandas
pip3.exe install scikit-learn
pip3.exe install sklearn
pip3.exe install tabulate
pip3.exe install tqdm
pause
