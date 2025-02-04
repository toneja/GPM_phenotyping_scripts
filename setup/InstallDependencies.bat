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
pip3.exe install pillow
pip3.exe install requests
pip3.exe install scikit-learn
pip3.exe install sklearn
pip3.exe install tabulate

REM Set the download URL and destination file
set downloadURL=https://wsr.imagej.net/distros/win/ij153-win-java8.zip
set destinationFile=ij153-win-java8.zip

REM Set the destination folder for unpacking ImageJ
set destinationFolder=..

REM Download the ImageJ package
echo Downloading ImageJ...
curl -o %destinationFile% %downloadURL%
if %errorlevel% neq 0 (
    echo Failed to download ImageJ.
    exit /b
)

REM Unpack the ImageJ package
echo Unpacking ImageJ...
powershell -Command "Expand-Archive -Path %destinationFile% -DestinationPath %destinationFolder% -Force"
if %errorlevel% neq 0 (
    echo Failed to unpack ImageJ.
    exit /b
)

REM Cleanup: Delete the downloaded zip file
echo Cleaning up...
del %destinationFile%

REM Done!
echo ImageJ has been downloaded and unpacked successfully.

REM make required subfolders
mkdir "..\ECHO Images" ..\results ..\ImageJ\GPM\images ..\ImageJ\GPM\results

echo Setup Complete!

pause
