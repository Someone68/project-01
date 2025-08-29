import os
import sys
import subprocess
import time
import re
import importlib.metadata
from import_utils import in_venv, create_venv, install_requirements, check_requirements

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def has_poetry():
    """Check if Poetry is installed on the system."""
    try:
        subprocess.check_call(
            ["poetry", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def run_with_poetry():
    print("Poetry detected! Using Poetry to manage dependencies...")
    subprocess.check_call(["poetry", "install"])
    print("Re-running via Poetry...")
    subprocess.check_call(["poetry", "run", "python", *sys.argv])
    sys.exit(0)

def init():
    if has_poetry():
        run_with_poetry()
        return

    # Fallback: your current venv + pip flow
    if not in_venv():
        python_in_venv = create_venv()
        print("Entering virtual environment...\n")
        subprocess.check_call([python_in_venv, *sys.argv])
        sys.exit(0)

    print("Checking dependencies...")
    install_required = check_requirements()

    if install_required:
        print("Installing required dependencies...")
        install_requirements(sys.executable)
        print("Package install successful!")
        time.sleep(1)

    cls()
