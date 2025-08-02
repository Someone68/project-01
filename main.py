import subprocess
import sys

from util import check_requirements, install_requirements, create_venv, cls

print("Checking dependencies...")

install_required = check_requirements()

if (install_required == 1):
    print("Missing packages, creating venv...")
    python_in_venv = create_venv()
    print("Installing required dependencies...")
    install_requirements(python_in_venv)
    print("Re-running script inside virtual environment...\n")
    subprocess.check_call([python_in_venv, *sys.argv])
    sys.exit(0)  # Prevent original script from continuing

cls();
