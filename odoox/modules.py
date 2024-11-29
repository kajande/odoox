import subprocess

import configparser
from pathlib import Path
import shutil


def execute(commands, options):
    if '-i' in options:
        module = options[options.index('-i')+1]
        install_module(module, options)

def uninstall_dependency(dep_module, dest_dir):
    """
    Removes a module from the destination directory if it exists.
    """
    module_path = dest_dir / dep_module
    if module_path.exists() and module_path.is_dir():
        try:
            shutil.rmtree(module_path)
            print(f"Uninstalled '{dep_module}'")
        except Exception as e:
            print(f"Error removing extra module '{dep_module}': {e}")


def install_module(module, options):
    """
    Copies specified modules from the source directory to the destination directory,
    and removes any extra modules not listed in the configuration file.
    """
    module_path = Path(f"./{module}")
    BASE_DEPS_DIR = Path("xaddons")
    DEST_DIR = Path("/mnt/extra-addons")

    config = configparser.ConfigParser()
    config.read(f"{module}/gitx.conf")

    dep_modules = set(config.sections())

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    # Find and remove extra modules
    existing_modules = {p.name for p in DEST_DIR.iterdir() if p.is_dir()}
    for extra_module in existing_modules - dep_modules - {module}:
        uninstall_dependency(extra_module, DEST_DIR)

    # Copy modules listed in the config file
    for dep_module in dep_modules:
        pull_uri = config[dep_module].get('pulluri', '')
        if not pull_uri:
            print(f"Warning: No pull URI defined for module '{dep_module}'")
            continue

        try:
            org, repo = pull_uri.split('/')[-2:]
            repo = repo.replace('.git', '')
            source_path = BASE_DEPS_DIR.joinpath(org, repo, dep_module)
            dest_path = DEST_DIR / dep_module

            # import ipdb;ipdb.set_trace()
            if not source_path.exists():
                subprocess.run(f"git clone {pull_uri} {BASE_DEPS_DIR/org/repo}".split())
                # continue

            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
            print(f"Installed '{dep_module}'")
        except Exception as e:
            print(f"Error processing module '{dep_module}': {e}")
    # Finally install the parent module
    shutil.copytree(module_path, DEST_DIR/module_path, dirs_exist_ok=True)
    print(f"Installed '{module}'")
