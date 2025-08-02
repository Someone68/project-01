import os
import sys
import re
import subprocess
import importlib.metadata

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_requirement(req_line):
    # Parse "package[extra]==version", "package>=version", etc.
    match = re.match(r"([a-zA-Z0-9_\-\.]+)", req_line)
    return match.group(1) if match else None

def check_requirements(requirements_file="requirements.txt"):
    try:
        with open(requirements_file) as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        for req in requirements:
            pkg_name = parse_requirement(req)
            if not pkg_name:
                continue  # skip malformed lines

            try:
                importlib.metadata.version(pkg_name)
            except importlib.metadata.PackageNotFoundError:
                print(f"Missing package: {pkg_name}")
                return 1

        return 0
    except Exception as e:
        print(f"Error checking requirements: {e}")
        return 1

def create_venv(venv_path="venv"):
    if not os.path.isdir(venv_path):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    return os.path.join(venv_path, "bin" if os.name != "nt" else "Scripts", "python")

def install_requirements(python_path):
    try:
        subprocess.check_call([python_path, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("There was an error while installing packages! I cannot continue!")
        sys.exit(1)
