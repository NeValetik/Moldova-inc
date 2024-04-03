import subprocess
import os
import shutil

def create_venv(venv_dir):
    """
    Create a virtual environment.
    """
    try:
        subprocess.run(["python", "-m", "venv", venv_dir], check=True)
    except:
        subprocess.run(["python3", "-m", "venv", venv_dir], check=True)

def install_libraries(venv_dir, requirements_file):
    """
    Install libraries from requirements.txt within the virtual environment.
    """
    subprocess.run([os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip"), "install", "-r", requirements_file], check=True)

def start_script(venv_dir, script_path):
    """
    Start another Python script within the virtual environment.
    """
    python_executable = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "python")
    subprocess.Popen([python_executable, script_path])

def delete_venv(venv_dir):
    """
    Delete the virtual environment.
    """
    shutil.rmtree(venv_dir)

def main():
    venv_dir = "temp_venv"  # Name of the virtual environment directory
    requirements_file = "requirements.txt"  # Path to requirements.txt
    script_path = "main.py"  # Path to the Python script you want to start

    # Create virtual environment
    create_venv(venv_dir)

    # Install libraries
    install_libraries(venv_dir, requirements_file)

    # Start another Python script within the virtual environment
    start_script(venv_dir, script_path)

    # Delete the virtual environment
    delete_venv(venv_dir)

if __name__ == "__main__":
    main()
