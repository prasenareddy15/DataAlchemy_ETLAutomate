@echo off

REM Navigate to the directory where the Python script is located
cd /d "C:\Path\To\Your\Python\code_1.py"

REM Activate the Python environment (if using a virtual environment)
REM call "C:\Path\To\Your\VirtualEnv\Scripts\activate.bat"

REM Run the Python script with the required arguments
python your_script.py --config_file "C:\Path\To\Config\config.json"

REM Deactivate the environment (optional)
call deactivate

REM Exit
exit
