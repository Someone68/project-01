import subprocess
import sys
import time
import os

from import_utils import check_requirements, install_requirements, create_venv, in_venv


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')



def init():
    if (not in_venv()):
        python_in_venv = create_venv()

        print("Entering virtual environment...\n")
        subprocess.check_call([python_in_venv, *sys.argv])
        sys.exit(0)  # prevent original from running

    print("Checking dependencies...")
    install_required = check_requirements()

    if (install_required):
        print("Installing required dependencies...")
        install_requirements(sys.executable)

        print("Package install successful!")
        time.sleep(1)

    cls();
