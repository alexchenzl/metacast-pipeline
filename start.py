import subprocess
import os
import sys
from datetime import datetime

def run_script(script_name):
    log_file = os.path.join("log", "output.log")
    with open(log_file, "a", encoding='utf-8') as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"\n{timestamp} - Running {script_name}\n")
        
        try:
            # Use subprocess.run instead of Popen for simpler error handling
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                check=True  # This will raise a CalledProcessError if the script fails
            )
            log.write(result.stdout)
            log.write(result.stderr)
            print(f"Successfully ran {script_name}")
        except subprocess.CalledProcessError as e:
            log.write(f"Error running {script_name}:\n")
            log.write(e.stdout)
            log.write(e.stderr)
            print(f"Error running {script_name}. Check log for details.")
            sys.exit(1)

def check_file(file_name):
    if not os.path.exists(file_name):
        print(f"Error: {file_name} not found. Stopping execution.")
        sys.exit(1)

# Ensure log directory exists
os.makedirs("log", exist_ok=True)

# List of scripts to run
scripts = [
    "0StepCleanTempData.py",
    "1DailyGetDataFormAirstack.py",
    "2Transform_data.py",
    "3GptCheckRelated.py",
    "4CheckKeywordManual.py",
    "5submitData.py"
]

# Files to check after certain scripts
file_checks = {
    "1DailyGetDataFormAirstack.py": "AllTrendOutput.txt",
    "2Transform_data.py": "transformed_json.txt",
    "3GptCheckRelated.py": "GptChecked.txt",
    "4CheckKeywordManual.py": "ManualChecked.txt"
}

# Run scripts and perform file checks
for script in scripts:
    run_script(script)
    if script in file_checks:
        check_file(file_checks[script])

print("All scripts executed successfully.")