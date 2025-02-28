import sys
import os
import subprocess


def create_symlink_for_hyphenated_dirs(base_path):
    """Finds directories with '-' in their name and creates a '_' symlink."""
    for name in os.listdir(base_path):
        full_path = os.path.join(base_path, name)

        if os.path.isdir(full_path) and "-" in name:
            symlink_name = name.replace("-", "_")
            symlink_path = os.path.join(base_path, symlink_name)

            if not os.path.exists(symlink_path):
                try:
                    os.symlink(full_path, symlink_path)
                    # print(f"Created symlink: {symlink_path} → {full_path}")
                except OSError as e:
                    # print(f"Failed to create symlink {symlink_name}: {e}")
                    pass


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


subprojects = ["../pytiling", "../pyglet-dragonbones"]

for subproject in subprojects:
    activate_subproject(
        os.path.abspath(os.path.join(os.path.dirname(__file__), subproject))
    )

suite_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if suite_path not in sys.path:
    sys.path.insert(0, suite_path)

try:
    import pytiling
    import pyglet_dragonbones
except ModuleNotFoundError:
    print("Using local versions of subprojects.")

    create_symlink_for_hyphenated_dirs(suite_path)
