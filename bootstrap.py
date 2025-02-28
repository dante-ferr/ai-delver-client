import sys
import os
import subprocess


def activate_subproject(env_path):
    try:
        venv_path = subprocess.check_output(
            ["pipenv", "--venv"], cwd=env_path, text=True
        ).strip()
        site_packages = os.path.join(venv_path, "lib/python3.x/site-packages")
        if site_packages not in sys.path:
            sys.path.insert(0, site_packages)
    except subprocess.CalledProcessError:
        print(f"Warning: No Pipenv environment found in {env_path}")


subprojects = ["../pytiling"]

for subproject in subprojects:
    activate_subproject(
        os.path.abspath(os.path.join(os.path.dirname(__file__), subproject))
    )

suite_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if suite_path not in sys.path:
    sys.path.insert(0, suite_path)

try:
    import pytiling
except ModuleNotFoundError:
    print("Using local version of pytiling")
